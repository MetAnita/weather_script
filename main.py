from datetime import date, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen
import mechanicalsoup
import os
from pathlib import Path
import time
import requests
import urllib


url = "https://new.meteo.lv/meteorologija-datu-meklesana/?nid=461"
# url = "https://www.meteo.lv/meteorologija-datu-meklesana/?nid=461"

page = None
while page is None:
    try:
        page = urlopen(url, timeout=30)
        print('page opne')
    except urllib.error.HTTPError:
        print('server error, lets try reopening page')
        time.sleep(5)
    except mechanicalsoup.utils.LinkNotFoundError:
        print('error, lets repeat opening')
        time.sleep(5)

# page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')

# headers for browser to prevent request blocking
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

# create directory for files
folder_path = Path('data', date.today().strftime('%Y%m%d'))
try:
    os.mkdir(folder_path)
except FileExistsError:
    print("Data folder already exists")


# dates for requests
today = date.today().strftime('%d.%m.%Y')  # datums līdz
yesterday = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')  # datums līdz
week_ago = (date.today() - timedelta(days=7)).strftime('%d.%m.%Y')  # datums no



'''Read historical weather data from meteo.lv'''


def read_weather_history(station, day_from, day_to, param1, param2, station_name):
    #create_request
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://new.meteo.lv/meteorologija-datu-meklesana/", headers=headers)
    browser.select_form('form[action="/meteorologija-datu-meklesana/?"]')

    #Fill web form
    browser["iBy"] = "station"
    browser["iStation"] = station
    browser["iParameter"] = (param1, param2)
    browser["iDateFrom"] = day_from
    browser["iDateTill"] = day_to
    response = browser.submit_selected()

    # create changeable file name
    filename = "%s.xls" % station_name
    completename = os.path.join(folder_path, filename)
    output = open(completename, 'wb')
    output.write(response.content)
    output.close()


# station_dict = {'Ainaži': 30000, 'Alūksne': 30004}    # smaller sample for tests and debug
station_dict = {'Ainaži': 30000, 'Alūksne': 30004, 'Bauska': 30011, 'Daugavpils': 30021, 'Dobele': 30022, 'Gulbene': 30034, 'Jelgava': 30036, 'Kalnciems': 30040, 'Kolka': 30046, 'Kuldīga': 30048, 'Lielpeči': 30058, 'Liepāja': 30060, 'Mērsrags': 30072, 'Pāvilosta': 30080, 'Piedruja': 30081, 'Rēzekne': 10000180, 'Rīga': 30096, 'Rūjiena': 30100, 'Saldus': 30102, 'Sigulda': 30103, 'Sīļi': 30104, 'Skrīveri': 30105, 'Stende': 30111, 'Vičaki': 30132, 'Zīlāni': 30140, 'Zosēni': 30141}
# station_dict = { 'Piedruja': 30081}




#+
for key, value in station_dict.items():
    print(key)
    print(value)
    time.sleep(10)   # to prevent DOS for website ;)
    while True:
        try:
            read_weather_history(str(value), week_ago, yesterday, "4001", "4570", key)
            print('try function')
        except urllib.error.HTTPError:
             print('server error, lets repeat request')
             time.sleep(5)
        except mechanicalsoup.utils.LinkNotFoundError:
            print('error, lets repeat')
            time.sleep(5)
        else:
            break


# read_weather_history('30141', week_ago, yesterday, "4001", "4570", 'Zosēni')

# temp = <option value="4001" selected="">Gaisa temperatūra, faktiskā</option>    # TODO: function to extract temperature option value
# rain = <option value="4570">Nokrišņu daudzums, stundas summa</option>           # TODO: function to extract mm rain option value

#TODO case 500 error, refresh and make second request ; LinkNotFoundError() ; urllib.error.HTTPError: HTTP Error 500: Internal Server Error
"""For development - to explore meteo.lv file download"""
import mechanicalsoup
from datetime import date, timedelta
import os
import requests
from pathlib import Path
import urllib
import time

yesterday = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')  # datums līdz

week_ago = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')  # datums no
print(week_ago)
#2024-08-11
station = 'Alūksne'

# headers for browser to prevent request blocking
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

# create directory for files
folder_path = Path('data', date.today().strftime('%Y%m%d'))

# https://videscentrs.lvgmc.lv/media/reports/station-report.xls?format=xls&mode=meteo&sakuma_datums=2024-08-05&beigu_datums=2024-08-11&stacija_id=30000&raditaja_id=4001
# https://videscentrs.lvgmc.lv/media/reports/station-report.xls?format=xls&mode=meteo&sakuma_datums=2024-08-05&beigu_datums=2024-08-11&stacija_id=30004&raditaja_id=4001

#gaisa temp faktiska raditaja_id=4001
#nokrišņki raditaja_id=4570

def read_weather_history(station, day_from, day_to, param1, param2, station_name):
    #create_request
    browser = mechanicalsoup.StatefulBrowser()

    # URL with parameters (use the provided arguments)
    url = (
        f"https://videscentrs.lvgmc.lv/media/reports/station-report.xls"
        f"?format=xls&mode=meteo&sakuma_datums={day_from}&beigu_datums={day_to}"
        f"&stacija_id={station}&raditaja_id={param1}"
    )
    print(url)
    response = browser.open(url, headers=headers)
    # Check if the response is successful
    if response.status_code == 200:
        # Create the file name
        filename = f"{station_name}.xls"
        print(filename)
        completename = os.path.join(folder_path, filename)
        print(completename)
        # Save the content to a file
        with open(completename, 'wb') as output:
            output.write(response.content)
            print("File saved successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

read_weather_history("30004", "2024-08-05", "2024-08-11", "4001", "4570", "Alūksne")

# create directory for files
folder_path = Path('data', date.today().strftime('%Y%m%d'))
try:
    os.mkdir(folder_path)
except FileExistsError:
    print("Data folder already exists")


# dates for requests
today = date.today().strftime('%Y-%m-%d')  # datums līdz
yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')  # datums līdz
week_ago = (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')  # datums no


'''Read historical weather data from videscentrs.lvgmc.lv'''


def read_weather_history(station, day_from, day_to, param1, param2, station_name):
    # Base URL template
    base_url = (
        "https://videscentrs.lvgmc.lv/media/reports/station-report.xls"
        "?format=xls&mode=meteo&sakuma_datums={day_from}&beigu_datums={day_to}"
        "&stacija_id={station}&raditaja_id={param}"
    )

    # Function to handle file download
    def download_file(param, param_suffix):
        # Construct the URL with the current param
        url = base_url.format(day_from=day_from, day_to=day_to, station=station, param=param)

        # Send the GET request
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            # Create the file name based on the param suffix
            filename = f"{station_name}_{param_suffix}.xlsx"
            completename = os.path.join(folder_path, filename)
            print(f"Saving to: {completename}")

            # Save the content to a file
            with open(completename, 'wb') as output:
                output.write(response.content)
                print(f"File {filename} saved successfully.")
        else:
            print(f"Failed to download the file for param {param}. Status code: {response.status_code}")

    # Download the first file with param1
    download_file(param1, "temp")

    # Download the second file with param2
    download_file(param2, "mm")


# station_dict = {'Ainaži': 30000, 'Alūksne': 30004}    # smaller sample for tests and debug
station_dict = {
    'Ainaži': 30000, 'Alūksne': 30004, 'Bauska': 30011, 'Daugavpils': 30021, 'Dobele': 30022, 'Gulbene': 30034,
    'Jelgava': 30036, 'Kalnciems': 30040, 'Kolka': 30046, 'Kuldīga': 30048, 'Lielpeči': 30058, 'Liepāja': 30060,
    'Mērsrags': 30072, 'Pāvilosta': 30080, 'Piedruja': 30081, 'Rēzekne': 10000180, 'Rīga': 30096, 'Rūjiena': 30100,
    'Saldus': 30102, 'Sigulda': 30103, 'Sīļi': 30104, 'Skrīveri': 30105, 'Stende': 30111, 'Vičaki': 30132,
    'Zīlāni': 30140, 'Zosēni': 30141
    }

#
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
        else:
            break


# read_weather_history('30141', week_ago, yesterday, "4001", "4570", 'Zosēni')
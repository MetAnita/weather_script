"""For development - to explore https://videscentrs.lvgmc.lv/ weather feature - temp & rain extraction """
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
# url example
# https://videscentrs.lvgmc.lv/laika-prognoze/Zīlāni

station_dict = {'Ainaži': '2-461628', 'Alūksne':'2-461528', 'Bauska': '2-461114', 'Daugavpils': '2-460413', 'Dobele': '2-460312', 'Gulbene': '2-459668', 'Jelgava': '2-459279', 'Kalnciems': '2-459102', 'Kolka': '2-458682', 'Kuldīga': '2-458460', 'Lielpeči': '2-457065', 'Liepāja': '5-2640600', 'Mērsrags': '2-457408', 'Pāvilosta': '2-456827', 'Piedruja': '2-456742', 'Rēzekne': '2-456202', 'Rīga': '2-456172', 'Rūjiena': '2-456008', 'Saldus': '2-455890', 'Sigulda': '2-455718', 'Sīļi': '2-455697', 'Skrīveri': '2-455523', 'Stende': '2-455260', 'Vičaki': '2-454251','Zīlāni': '2-453862','Zosēni': '2-453822'}


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
#
url = requests.get("https://videscentrs.lvgmc.lv/laika-prognoze/Ainaži", headers=headers)
soup = BeautifulSoup(url.content, "lxml")
print(soup.prettify())


def test_urls(st_dict):
    for key in station_dict:
        url = "https://www.yr.no/en/forecast/daily-table/%s" % key
        print(url)
        url = requests.get("https://videscentrs.lvgmc.lv/laika-prognoze/Kolka", headers=headers)
        soup = BeautifulSoup(url.content, "lxml")
        print(soup.prettify())


# test_urls(station_dict)

res = soup.find_all('div', ["weather-daily-details-prop"])
print('test the temperature')
for temp in res:
    t_value = temp.text
    print(t_value)

    # < script src = "/index.c8ed00.js" type = "text/javascript" >
    # < script src = "/index.c8ed00.js" type = "text/javascript" >
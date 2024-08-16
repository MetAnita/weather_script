"""For development - to explore https://www.accuweather.com weather feature - temp & rain extraction """

from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time

station_dict = {'Ainaži': '2-461628', 'Alūksne':'2-461528', 'Bauska': '2-461114', 'Daugavpils': '2-460413', 'Dobele': '2-460312', 'Gulbene': '2-459668', 'Jelgava': '2-459279', 'Kalnciems': '2-459102', 'Kolka': '2-458682', 'Kuldīga': '2-458460', 'Lielpeči': '2-457065', 'Liepāja': '5-2640600', 'Mērsrags': '2-457408', 'Pāvilosta': '2-456827', 'Piedruja': '2-456742', 'Rēzekne': '2-456202', 'Rīga': '2-456172', 'Rūjiena': '2-456008', 'Saldus': '2-455890', 'Sigulda': '2-455718', 'Sīļi': '2-455697', 'Skrīveri': '2-455523', 'Stende': '2-455260', 'Vičaki': '2-454251','Zīlāni': '2-453862','Zosēni': '2-453822'}
sample_dict = {'Alūksne':'aluksne/2-222319_1_al/daily-weather-forecast/2-222319_1_al', 'Bauska': 'bauska/222828/daily-weather-forecast/222828' }


options = Options()
options.headless = True
browser = Firefox(options=options)

url = "https://www.accuweather.com/en/lv/bauska/222828/weather-forecast/222828"
browser.get(url)
time.sleep(10)   # to fully load data
html = browser.execute_script("return document.documentElement.innerHTML")
#print(html)
sel_soup = BeautifulSoup(html, 'html.parser')
print(sel_soup.prettify())


# headers = {
#     'Access-Control-Allow-Origin': '*',
#     'Access-Control-Allow-Methods': 'GET',
#     'Access-Control-Allow-Headers': 'Content-Type',
#     'Access-Control-Max-Age': '3600',
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
#     }
# #
# url = requests.get("https://www.accuweather.com/en/lv/bauska/222828/weather-forecast/222828", headers=headers)
# soup = BeautifulSoup(url.content, "lxml")
# print(soup.prettify())
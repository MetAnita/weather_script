"""For development - to explore https://videscentrs.lvgmc.lv/ weather feature - temp & rain extraction """
from bs4 import BeautifulSoup
from requests_html import HTMLSession  #to get data from javascript based page
from urllib.request import urlopen
import requests
import json
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import re

options = Options()
options.headless = True
browser = Firefox(options=options)

url = "https://videscentrs.lvgmc.lv/laika-prognoze/Zīlāni"
browser.get(url)
time.sleep(10)   # to fully load data
html = browser.execute_script("return document.documentElement.innerHTML")
# print(html)
sel_soup = BeautifulSoup(html, 'html.parser')
# print(sel_soup.prettify())

station_dict = {'Ainaži': '2-461628', 'Alūksne':'2-461528', 'Bauska': '2-461114', 'Daugavpils': '2-460413', 'Dobele': '2-460312', 'Gulbene': '2-459668', 'Jelgava': '2-459279', 'Kalnciems': '2-459102', 'Kolka': '2-458682', 'Kuldīga': '2-458460', 'Lielpeči': '2-457065', 'Liepāja': '5-2640600', 'Mērsrags': '2-457408', 'Pāvilosta': '2-456827', 'Piedruja': '2-456742', 'Rēzekne': '2-456202', 'Rīga': '2-456172', 'Rūjiena': '2-456008', 'Saldus': '2-455890', 'Sigulda': '2-455718', 'Sīļi': '2-455697', 'Skrīveri': '2-455523', 'Stende': '2-455260', 'Vičaki': '2-454251','Zīlāni': '2-453862','Zosēni': '2-453822'}


def test_urls(st_dict):
    for key in station_dict:
        url = "https://videscentrs.lvgmc.lv/laika-prognoze/%s" % key
        print(url)
        # url = requests.get("https://videscentrs.lvgmc.lv/laika-prognoze/Kolka")
        soup = BeautifulSoup(url.content, "lxml")
        print(soup.prettify())


# test_urls(station_dict)


each_day = sel_soup.find_all("div", class_="weather-daily-details-item")



print('test the temp - day and night full text')
for t in each_day:
    t_value = t.text
    print(t_value)

# temperature example from webpage
# <div class="weather-daily-details-prop"><div><span class="emphasis">-13</span> °C</div></div>

print('test the temp - day and night values')

t_list=[]

for t in each_day[1:]:  #[1:] to skip first entry that is for today
    t_val=t.span.text
    t_list.append(t_val)
    print(t_val)
    # print(t.contents[0])
    # print(t.contents[1])
    # print(t.contents[2])
    # print(t.contents[3])

# a[start_index:end_index:step]
# split day and night values
t_list_day = t_list[::2]
print(t_list_day)
t_list_night = t_list[1::2]
print(t_list_night)

# nokrišņi example from webpage
# < div class ="weather-daily-details-prop" > < div >
# < span class ="emphasis" >0< / span >mm< / div >< span > nokrišņu< / span >

nokrisni = sel_soup.find_all("span", string="nokrišņu")
print('test the rain')

new_nokr = [ mm.previous_sibling for mm in nokrisni ]

for rain in new_nokr:
    # r_value = rain.text
    r_value = rain.contents[0].text
    print(r_value)


# validate list length
TestLong=['-12', '-12', '0', '0', '0', '0', '-1', '-1', '-4', '-4', '-4', '-4', '-2', '-2', '1', '1', '1', '1']
TestMMLong = [0.0, 0.0, 2.0, 2.0, 1.0, 1.0, 8.0, 8.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.6, 0.5, 0.5, 0.0, 0.0]
TestShort = []
TestMMShort = []
TestNorm =['2', '3', '2', '3', '4', '6', '7', '7', '7']
TestMMNorm=[0.0, 0.1, 0.0, 0.2, 0.6, 0.6, 0.0, 0.0, 0.0]

def check_list_len(l):
    print('start check list length')
    if len(l)==9:
        print('OK 9 simbols')
    elif len(l)<9:
        print('Too short')
        l = [""] * 9
    elif len(l)>9:
        print('Too long')
        l = [""] * 9
    return l


print(check_list_len(TestLong))
print(check_list_len(TestMMLong))
print(check_list_len(TestShort))
print(check_list_len(TestMMShort))
print(check_list_len(TestNorm))
print(check_list_len(TestMMNorm))



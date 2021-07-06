"""For development - to explore gismeteo.lv weather feature - temp & rain extraction """
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
# url examples
# https://www.gismeteo.lv/weather-aluksne-4124/2-weeks/
# https://www.gismeteo.lv/weather-mersrags-47065/2-weeks/

station_dict = {'Ainaži': 'ainazi-47075', 'Alūksne': 'aluksne-4124', 'Bauska': 'bauska-4139', 'Daugavpils': 'daugavpils-4177', 'Dobele': 'dobele-4137', 'Gulbene': 'gulbene-4125', 'Jelgava': 'jelgava-4138', 'Kalnciems': 'kalnciems-322319', 'Kolka': 'kolka-47057', 'Kuldīga': 'kuldiga-4106', 'Lielpeči': 'ogre-47066', 'Liepāja': 'liepaja-4134', 'Mērsrags': 'mersrags-47065', 'Pāvilosta': 'pavilosta-47067', 'Piedruja': 'piedruja-322361', 'Rēzekne': 'rezekne-4140', 'Rīga': 'riga-4136', 'Rūjiena': 'rujiena-47073', 'Saldus': 'saldus-4135', 'Sigulda': 'sigulda-4103', 'Sīļi': 'silajani-322513', 'Skrīveri': 'skriveri-322563', 'Stende': 'stende-47083', 'Vičaki': 'ventspils-4123', 'Zīlāni': 'zilani-322369', 'Zosēni': 'vecpiebalga-322623'}

sample_dict = {'Ainaži': 'ainazi-47075'}
val = sample_dict['Ainaži']
url = "https://www.gismeteo.lv/weather-%s/2-weeks/" % val
print(url)

# Nokrišņu daudzums, mm
# <div class="w_prec__value">0</div>
# < div class ="w_prec__value" style="bottom: 3px" >0, 9< / div >

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

url = requests.get("https://www.gismeteo.lv/weather-aluksne-4124/2-weeks/", headers=headers)
soup = BeautifulSoup(url.content, "lxml")
# print(soup.prettify())

# vidējā diennakts temperatūra
temp_tag = soup.find('div', ["widget__row widget__row_averageTemp"])
temp_values = temp_tag.find_all('span', ['unit unit_temperature_c'])
print('test the temperature')

for temp in temp_values:
    t_value = temp.text
    print(t_value)

print('test the temperature - 10 days')
# vidējā diennakts temperatūra - 10 day value
for temp in temp_values[1:-3]:
    t_value = temp.text
    print(t_value)

# Nokrišņu daudzums, mm
print('test the rain ')
test_rain = soup.find_all('div', ["w_prec__value"])
for rain in test_rain:
    value = rain.text
    print(value.strip())

# Nokrišņu daudzums, mm - 10 days forecast
print('test the rain - 10 days')
test_rain = soup.find_all('div', ["w_prec__value"])
for rain in test_rain[1:-3]:
    value = rain.text
    print(value.strip())

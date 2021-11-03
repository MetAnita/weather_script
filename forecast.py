'''''Acquire weather forecast from gismeteo.lv'''
from bs4 import BeautifulSoup
import requests
import time
import unicodedata as ud


station_dict = {'Ainaži': 'ainazi-47075', 'Alūksne': 'aluksne-4124', 'Bauska': 'bauska-4139', 'Daugavpils': 'daugavpils-4177', 'Dobele': 'dobele-4137', 'Gulbene': 'gulbene-4125', 'Jelgava': 'jelgava-4138', 'Kalnciems': 'kalnciems-322319', 'Kolka': 'kolka-47057', 'Kuldīga': 'kuldiga-4106', 'Lielpeči': 'ogre-47066', 'Liepāja': 'liepaja-4134', 'Mērsrags': 'mersrags-47065', 'Pāvilosta': 'pavilosta-47067', 'Piedruja': 'piedruja-322361', 'Rēzekne': 'rezekne-4140', 'Rīga': 'riga-4136', 'Rūjiena': 'rujiena-47073', 'Saldus': 'saldus-4135', 'Sigulda': 'sigulda-4103', 'Sīļi': 'silajani-322513', 'Skrīveri': 'skriveri-322563', 'Stende': 'stende-47083', 'Vičaki': 'ventspils-4123', 'Zīlāni': 'zilani-322369', 'Zosēni': 'vecpiebalga-322623'}

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

my_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"}


def temp_10_day_forecast(station):
    station_val_list = []
    val = station_dict[station]
    url = "https://www.gismeteo.lv/weather-%s/2-weeks/" % val
    print('Getting: ', url)
    url_station = requests.get(url, headers=headers)
    soup = BeautifulSoup(url_station.content, "lxml")
    temp_tag = soup.find('div', ["widget-row-chart widget-row-chart-temperature-avg"])
    temp_values = temp_tag.find_all('span', ['unit unit_temperature_c'])
    print('test the temperature')
    for temp in temp_values[1:-3]:
        t_value = temp.text
        # print(type(t_value))
        # t_value.encode('utf-8')
        # print(repr(t_value.encode('utf-8')))
        t_value.replace('−', '-')
        print(t_value)
        station_val_list.append(int(t_value))
        # station_val_list.append(t_value)
    return station_val_list


def mm_temp_10_day_forecast(station):
    t_list = []
    mm = []
    val = station_dict[station]
    url = "https://www.gismeteo.lv/weather-%s/2-weeks/" % val
    print('Getting: ', url)
    url_station = requests.get(url, headers=my_headers)
    soup = BeautifulSoup(url_station.content, "lxml")
    temp_tag = soup.find('div', ["widget-row-chart widget-row-chart-temperature-avg"])  #27.10 change in gismeteo.lv homepage
    temp_values = temp_tag.find_all('span', ['unit unit_temperature_c'])
    for temp in temp_values[1:-3]:
        t_val = temp.text
        t_val.encode('utf-8')
       # t_value.replace('−', U'-')  # doesnt work
        if ud.name(t_val[0]) == 'MINUS SIGN':
            print('Changing minus sign')
            t_value = "-" + t_val[1:]  # changing minus sign
        else: t_value = t_val
        t_value = int(t_value)
        t_list.append(int(t_value))  # encoding problems for minus sign −1
        # t_list.append(t_value)
    rain_tag = soup.find_all('div', ["widget-row widget-row-precipitation-bars row-with-caption"])  #27.10 change in gismeteo.lv homepage
    test_rain = rain_tag[0].find_all('div', ["row-item"])
    for rain in test_rain[1:-3]:
        mm_value = rain.text.strip()
        mm_num = float(mm_value.replace(',', '.'))      # to convert string to float
        mm.append(float(mm_num))
    print(station, '  C temp for 10 days: ', t_list)
    print(station, ' mm rain for 10 days: ', mm)
    if not mm:
        print('Did not get mm valus -> filling with zeroes')
        mm = [0]*10

    return t_list, mm


def temp_forecast(station_dict):
    stations_temp = []
    for key in station_dict:
        print('Getting data for: ', key)
        t = temp_10_day_forecast(key)
        stations_temp.append(t)
        time.sleep(10)
    return stations_temp


dupl_st = ['Bauska', 'Gulbene', 'Kuldīga', 'Rūjiena', 'Stende']
tripl_st = ['Zīlāni', 'Zosēni']


def temp_forecast_duplicates(station_dict, dupl, tripl):
    stations_temp = []
    for key in station_dict:
        print('Getting data for: ', key)
        t = temp_10_day_forecast(key)
        if key in dupl:
            print('Appending 2x data for: ', key,' to comply with excel structure' )
            stations_temp.extend(2 * t)
        elif key in tripl:
            print('Appending 3x data for: ', key, ' to comply with excel structure')
            stations_temp.extend(3 * t)
        else:
            print('Appending data')
            stations_temp.extend(t)
        time.sleep(10)
    return stations_temp


def mm_temp_forecast_duplicates(station_dict, dupl, tripl):
    stations_temp = []
    stations_mm = []
    for key in station_dict:
        print('Getting data for: ', key)
        t, mm = mm_temp_10_day_forecast(key)
        if key in dupl:
            print('Appending 2x data for: ', key,' to comply with excel structure' )
            stations_temp.extend(2 * t)
            stations_mm.extend(2 * mm)
        elif key in tripl:
            print('Appending 3x data for: ', key, ' to comply with excel structure')
            stations_temp.extend(3 * t)
            stations_mm.extend(3 * mm)
        else:
            print('Appending data')
            stations_temp.extend(t)
            stations_mm.extend(mm)
        time.sleep(10)
    return stations_temp, stations_mm

# print(temp_forecast(station_dict))
# print(temp_10_day_forecast('Rūjiena'))
# print(temp_forecast_duplicates(station_dict, dupl_st, tripl_st))
# print(mm_temp_forecast_duplicates(station_dict, dupl_st, tripl_st))


# workaround for minus sign error
# SyntaxError: invalid character '−' (U+2212)
data = '−1'
if ud.name(data[0])=='MINUS SIGN':
    print('True')
    s= "-" + data[1:]    #changing minus sign

#ud.UCD
print (repr(ud.name(data[0]))) # Hyphen in string data
print (repr(ud.name(s[0]))) # Hyphen in new string data
print (repr(ud.name(u'-')))    # An ascii hyphen



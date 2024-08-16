"""For development - to explore https://www.yr.no/ weather feature - temp & rain extraction """
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import json
# url example
# https://www.yr.no/en/forecast/daily-table/2-453822/Latvia/Jaunpiebalga/Zosēnu%20pagasts/Zosēni


# station_dict = {'Ainaži': 'Salacgrīvas/Ainaži/Ainaži', 'Alūksne':'Aluksnes/Alūksne/Alūksne', 'Bauska': 'Bauskas%20Rajons/Bauska/Bauska', 'Daugavpils': 'Daugavpils%20municipality/Daugavpils', 'Dobele': 'Dobeles/Dobele/Dobele', 'Gulbene': 'Gulbenes/Gulbene/Gulbene', 'Jelgava': 'Jelgava/Jelgava/Jelgava', 'Kalnciems': 'Jelgava%20fylke/Kalnciema%20pagasts/Kalnciems', 'Kolka': 'Dundaga/Kolkas%20pagasts/Kolka', 'Kuldīga': 'Kuldigas/Kuldīga/Kuldīga', 'Lielpeči': 'Ogre/Ogre/Ogre', 'Liepāja': 'Liepaja', 'Mērsrags': 'Mesraga/Mērsraga%20novads/Mērsrags', 'Pāvilosta': 'Pāvilostas/Pāvilosta/Pāvilosta', 'Piedruja': 'Daugavpils%20municipality/Piedruja', 'Rēzekne': 'Rezekne/Rēzekne/Rēzekne', 'Rīga': 'Riga/Rīga/Riga', 'Rūjiena': 'Rūjienas/Rūjiena/Rūjiena', 'Saldus': 'Saldus%20Rajons/Saldus/Saldus', 'Sigulda': 'Sigulda/Sigulda/Sigulda', 'Sīļi': 'Preilu/Silajāni', 'Skrīveri': 'Skrīveri/Skrīveru%20novads/Skrīveri', 'Stende': 'Talsi%20Municipality/Stende/Stende', 'Vičaki': 'Ventspils%20Rajons/Ances%20pagasts/Vičaki','Zīlāni': 'Jēkabpils%20Municipality/Zilāni','Zosēni': 'Jaunpiebalga/Zosēnu%20pagasts/Zosēni'}
station_dict = {'Ainaži': '2-461628', 'Alūksne':'2-461528', 'Bauska': '2-461114', 'Daugavpils': '2-460413', 'Dobele': '2-460312', 'Gulbene': '2-459668', 'Jelgava': '2-459279', 'Kalnciems': '2-459102', 'Kolka': '2-458682', 'Kuldīga': '2-458460', 'Lielpeči': '2-457065', 'Liepāja': '5-2640600', 'Mērsrags': '2-457408', 'Pāvilosta': '2-456827', 'Piedruja': '2-456742', 'Rēzekne': '2-456202', 'Rīga': '2-456172', 'Rūjiena': '2-456008', 'Saldus': '2-455890', 'Sigulda': '2-455718', 'Sīļi': '2-455697', 'Skrīveri': '2-455523', 'Stende': '2-455260', 'Vičaki': '2-454251','Zīlāni': '2-453862','Zosēni': '2-453822'}


sample_dict = {'Ainaži': 'Salacgrīvas/Ainaži/Ainaži', 'Alūksne':'Aluksnes/Alūksne/Alūksne', 'Bauska': 'Bauskas%20Rajons/Bauska/Bauska','Zīlāni': 'Jēkabpils%20Municipality/Zilāni' }

# Nokrišņu daudzums, mm
# <span class="precipitation precipitation--hidden precipitation--color" role="text"><span class="nrk-sr">Precipitation </span><span class="precipitation__value">0</span><abbr class="precipitation__unit" title="millimeters">mm</abbr></span>

# <span class="Precipitation-module__main-sU6qN" role="text" data-tone="primary" data-invisible="false"><span class="nrk-sr">Nedbør </span><span>5,1</span><abbr class="Precipitation-module__unit-Oe12G" title="millimeter">mm</abbr></span>
# <span class="nrk-sr">Nedbør </span>
# <span>5,1</span>

# temperatūra max min
# <span class="min-max-temperature"><span class="temperature min-max-temperature__max temperature--warm" role="text">27<span class="temperature__degree" title="degrees celsius" aria-label="degrees celsius">°</span></span><span class="min-max-temperature__separator">/</span>
# <span class="temperature min-max-temperature__min temperature--warm" role="text">20<span class="temperature__degree" title="degrees celsius" aria-label="degrees celsius">°</span></span></span>


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
#
url = requests.get("https://www.yr.no/en/forecast/daily-table/2-458682/Latvia/Dundaga/Kolkas%20pagasts/Kolka", headers=headers)
soup = BeautifulSoup(url.content, "lxml")
#print(soup.prettify())
#
#
# # temperatūra
#
# res = soup.find_all('span', ["min-max-temperature"])
# print('test the temperature')
# for temp in res:
#     t_value = temp.text
#     print(t_value)
#
# # maksimālā un minimālā temperatūra
# res_max = soup.find_all('span', ["temperature min-max-temperature__max temperature--warm"])
# res_min = soup.find_all('span', ["temperature min-max-temperature__min temperature--warm"])
#
# # mm
#mm = soup.find_all('span', {"class":"Precipitation-module__main-sU6qN"})
print('test new mm')
# Find the outer div with the class name 'daily-weather-list-item__precipitation'
divs = soup.find_all('div', class_='daily-weather-list-item__precipitation')

precipitation_values = []

for div in divs:
    # Find the span that contains the precipitation value
    span = div.find('span', class_='Precipitation-module__main-sU6qN')
    if span:
        value_span = span.find_all('span')[1]  # The value is in the second span
        value = value_span.get_text(strip=True)
        precipitation_values.append(value)

print(precipitation_values)




# print('test the temperature - calculate avg')
# for min_temp, max_temp in zip(res_min[1:], res_max[1:]):
#     #sākas ar šodienu
#     min_t = min_temp.contents[0]
#     max_t = max_temp.contents[0]
#     avg_temp = (int(min_t) + int(max_t))/2
#     # print(avg_temp)
#     print(min_temp.contents[0], int(min_temp.contents[0]),  max_temp.contents[0], int(max_temp.contents[0]))
#




def test_urls(st_dict):
    for key in station_dict:
        val = st_dict[key]
        url = "https://www.yr.no/en/forecast/daily-table/%s"
        print(url)


def mm_temp_8_day_forecast(station):
    """"get 8 day forecast from yr.no for single station"""
    t_list_min = []
    t_list_max = []
    t_list_avg = []
    mm = []
    val = station_dict[station]
    url = "https://www.yr.no/en/forecast/daily-table/%s" % val
    print('Getting: ', url)
    url_station = requests.get(url, headers=headers)
    soup = BeautifulSoup(url_station.content, "lxml")

    res_max = soup.find_all('span', {'class': re.compile(r'^temperature min-max-temperature__max temperature')})
    res_min = soup.find_all('span', {'class': re.compile(r'^temperature min-max-temperature__min temperature')})
    res_mm_divs = soup.find_all('div', class_='daily-weather-list-item__precipitation')


    for div in res_mm_divs[1:]: # skip today
        # Find the span that contains the precipitation value
        span = div.find('span', class_='Precipitation-module__main-sU6qN')
        if span:
            value_span = span.find_all('span')[1]  # The value is in the second span
            value = value_span.get_text(strip=True)
            value = float(value.replace(',', '.'))  # to convert string to float
            mm.append(value)

    print(mm)


    for min_temp, max_temp in zip(res_min[1:], res_max[1:]): #start with tomorrow
        min_t = min_temp.contents[0]
        max_t = max_temp.contents[0]
        avg_temp = (int(min_t) + int(max_t)) / 2
        t_list_min.append(int(min_t))
        t_list_max.append(int(max_t))
        t_list_avg.append(int(avg_temp))

    print(station, '  C min temp for 8 days: ', t_list_min)
    print(station, '  C max temp for 8 days: ', t_list_max)
    print(station, '  C avg temp for 8 days: ', t_list_avg)
    print(station, ' mm rain for 8 days: ', mm)

    return t_list_min, t_list_max, t_list_avg, mm

mm_temp_8_day_forecast("Mērsrags")

#
# def mm_temp_8_day_forecast(station):
#     """"get 9 day forecast from yr.no for single station"""
#     t_list_min = []
#     t_list_max = []
#     t_list_avg = []
#     mm = []
#     val = STATION_DICT[station]
#     url = "https://www.yr.no/en/forecast/daily-table/%s" % val
#     print('Getting: ', url)
#     url_station = requests.get(url, headers=HEADERS)
#     soup = BeautifulSoup(url_station.content, "lxml")
#     res_max = soup.find_all('span', {'class': re.compile(r'^temperature min-max-temperature__max temperature')})
#     res_min = soup.find_all('span', {'class': re.compile(r'^temperature min-max-temperature__min temperature')})
#     res_mm_divs = soup.find_all('div', class_='daily-weather-list-item__precipitation')
#
#     for div in res_mm_divs[1:]:  # skip today
#         # Find the span that contains the precipitation value
#         span = div.find('span', class_='Precipitation-module__main-sU6qN')
#         if span:
#             value_span = span.find_all('span')[1]  # The value is in the second span
#             value = value_span.get_text(strip=True)
#             value = float(value.replace(',', '.'))  # to convert string to float
#             mm.append(value)
#
#     for min_temp, max_temp in zip(res_min[1:], res_max[1:]):  #start with tomorrow
#         min_t = min_temp.contents[0]
#         max_t = max_temp.contents[0]
#         avg_temp = (int(min_t) + int(max_t)) / 2
#         t_list_min.append(int(min_t))
#         t_list_max.append(int(max_t))
#         t_list_avg.append(int(avg_temp))
#
#     print(station, '  C min temp for 9 days: ', t_list_min)
#     print(station, '  C max temp for 9 days: ', t_list_max)
#     print(station, '  C avg temp for 9 days: ', t_list_avg)
#     print(station, ' mm rain for 9 days: ', mm)
#
#     return t_list_avg, mm
#
#
# mm_temp_8_day_forecast("Piedruja")
# # mm_temp_8_day_forecast("Alūksne")
#
#
# def mm_temp_forecast_duplicates(station_dict, dupl, tripl):
#     """"Modify data by adding duplicate values and empty values to comply with excel structure"""
#     stations_temp = []
#     stations_mm = []
#     for key in station_dict:
#         print('Getting data for: ', key)
#         t, mm = mm_temp_8_day_forecast(key)
#         t.append("")   # dirty solution to add  blank value
#         mm.append("")
#         if key in dupl:
#             print('Appending 2x data for: ', key, ' to comply with excel structure')
#             stations_temp.extend(2 * t)
#             stations_mm.extend(2 * mm)
#         elif key in tripl:
#             print('Appending 3x data for: ', key, ' to comply with excel structure')
#             stations_temp.extend(3 * t)
#             stations_mm.extend(3 * mm)
#         else:
#             print('Appending data')
#             stations_temp.extend(t)
#             stations_mm.extend(mm)
#         time.sleep(10)
#     return stations_temp, stations_mm
#
#
# # print(mm_temp_forecast_duplicates(station_dict, dupl_st, tripl_st))
# def update_forecast_yr(filename):
#     wb_obj = openpyxl.load_workbook(filename)
#     # Read the forecast sheet t_mm_prognoze
#     sheet = wb_obj["t_mm_prognoze"]
#     listt, listmm = mm_temp_forecast_duplicates(STATION_DICT, dupl_st, tripl_st)
#
#     for i in range(3, 353):
#         l = i - 3
#         cellref_t = sheet.cell(row=i, column=10)     # writing temp to J column
#         cellref_t.value = listt[l]
#         cellref_mm = sheet.cell(row=i, column=11)    # writing mm to K column
#         cellref_mm.value = listmm[l]
#
#     wb_obj.save(filename)
#
#
# update_forecast_yr(completename)

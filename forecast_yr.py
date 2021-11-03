'''''Acquire weather forecast from yr.no and write in results excel file'''
from bs4 import BeautifulSoup
import requests
import time
import re
import openpyxl
from write_info import completename, dupl_st, tripl_st

station_dict = {'Ainaži': '2-461628', 'Alūksne':'2-461528', 'Bauska': '2-461114', 'Daugavpils': '2-460413', 'Dobele': '2-460312', 'Gulbene': '2-459668', 'Jelgava': '2-459279', 'Kalnciems': '2-459102', 'Kolka': '2-458682', 'Kuldīga': '2-458460', 'Lielpeči': '2-457065', 'Liepāja': '5-2640600', 'Mērsrags': '2-457408', 'Pāvilosta': '2-456827', 'Piedruja': '2-456742', 'Rēzekne': '2-456202', 'Rīga': '2-456172', 'Rūjiena': '2-456008', 'Saldus': '2-455890', 'Sigulda': '2-455718', 'Sīļi': '2-455697', 'Skrīveri': '2-455523', 'Stende': '2-455260', 'Vičaki': '2-454251','Zīlāni': '2-453862','Zosēni': '2-453822'}

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

my_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"}


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
    res_mm = soup.find_all('span', ["precipitation__value"])

    for m in res_mm[2:]:
        m_value = m.text
        m_value = float(m_value.replace(',', '.'))  # to convert string to float
        mm.append(float(m_value))

    for min_temp, max_temp in zip(res_min[1:], res_max[1:]): #start with tomorrow
        min_t = min_temp.contents[0]
        max_t = max_temp.contents[0]
        avg_temp = (int(min_t) + int(max_t)) / 2
        # t_list_min.append(int(min_t))
        # t_list_max.append(int(max_t))
        t_list_avg.append(int(avg_temp))

    # print(station, '  C min temp for 8 days: ', t_list_min)
    # print(station, '  C max temp for 8 days: ', t_list_max)
    print(station, '  C avg temp for 8 days: ', t_list_avg)
    print(station, ' mm rain for 8 days: ', mm)

    return t_list_avg, mm

# mm_temp_8_day_forecast("Piedruja")
# mm_temp_8_day_forecast("Alūksne")


def mm_temp_forecast_duplicates(station_dict, dupl, tripl):
    """"Modify data by adding duplicate values and empty values to comply with excel structure"""
    stations_temp = []
    stations_mm = []
    for key in station_dict:
        print('Getting data for: ', key)
        t, mm = mm_temp_8_day_forecast(key)
        t.append("")   # dirty solution to add two blank values
        t.append("")
        mm.append("")
        mm.append("")
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


# print(mm_temp_forecast_duplicates(station_dict, dupl_st, tripl_st))
def update_forecast_yr(filename):
    wb_obj = openpyxl.load_workbook(filename)
    # Read the forecast sheet t_mm_prognoze
    sheet = wb_obj["t_mm_prognoze"]
    listt, listmm = mm_temp_forecast_duplicates(station_dict, dupl_st, tripl_st)

    for i in range(3, 353):
        l = i - 3
        cellref_t = sheet.cell(row=i, column=10)     # writing temp to J column
        cellref_t.value = listt[l]
        cellref_mm = sheet.cell(row=i, column=11)    # writing mm to K column
        cellref_mm.value = listmm[l]

    wb_obj.save(filename)


update_forecast_yr(completename)
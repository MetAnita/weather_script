'''''Acquire weather forecast from https://videscentrs.lvgmc.lv'''
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import openpyxl
from write_info import completename, dupl_st, tripl_st

station_dict = {'Ainaži': '2-461628', 'Alūksne':'2-461528', 'Bauska': '2-461114', 'Daugavpils': '2-460413', 'Dobele': '2-460312', 'Gulbene': '2-459668', 'Jelgava': '2-459279', 'Kalnciems': '2-459102', 'Kolka': '2-458682', 'Kuldīga': '2-458460', 'Lielpeči': '2-457065', 'Liepāja': '5-2640600', 'Mērsrags': '2-457408', 'Pāvilosta': '2-456827', 'Piedruja': '2-456742', 'Rēzekne': '2-456202', 'Rīga': '2-456172', 'Rūjiena': '2-456008', 'Saldus': '2-455890', 'Sigulda': '2-455718', 'Sīļi': '2-455697', 'Skrīveri': '2-455523', 'Stende': '2-455260', 'Vičaki': '2-454251','Zīlāni': '2-453862','Zosēni': '2-453822'}

options = Options()
options.headless = True
browser = Firefox(options=options)


def test_urls(st_dict):
    for key in station_dict:
        url = "https://videscentrs.lvgmc.lv/laika-prognoze/%s" % key
        print(url)
        browser.get(url)
        time.sleep(10)  # to fully load data
        html = browser.execute_script("return document.documentElement.innerHTML")
        sel_soup = BeautifulSoup(html, 'html.parser')
        print(sel_soup.prettify())


# test_urls(station_dict)

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def mm_temp_9_day_forecast(station):
    """"get 9 day forecast from lvgmc for single station"""
    t_list = []
    r_list = []
    url = "https://videscentrs.lvgmc.lv/laika-prognoze/%s" % station
    print('Getting: ', url)
    browser.get(url)
    time.sleep(10)  # to fully load data
    html = browser.execute_script("return document.documentElement.innerHTML")
    sel_soup = BeautifulSoup(html, 'html.parser')
    each_day = sel_soup.find_all("div", class_="weather-daily-details-item")

    for t in each_day[2:]:  # [1:] to start with tomorrow
        t_val = t.span.text
        t_list.append(t_val)
    t_list_night = t_list[::2]
    t_list_day = t_list[1::2]

    nokrisni = sel_soup.find_all("span", string="nokrišņu")
    new_nokr = [mm.previous_sibling for mm in nokrisni]

    for rain in new_nokr[2:]: # [1:] to start with tomorrow
        r_value = rain.contents[0].text
        if is_float(r_value):
            r_list.append(float(r_value))
        else:
            r_list.append("")
        # try:
        #     float(r_value)
        # except ValueError:
        #     r_value=0.0
        # r_list.append(float(r_value))
    mm_night = r_list[::2]
    mm_day = r_list[1::2]

    print(station, '  C day temp for 9 days: ', t_list_day)
    print(station, '  C night temp for 9 days: ', t_list_night)
    print(station, '  mm day for 9 days: ', mm_day)
    print(station, '  mm night for 9 days: ', mm_night)

    return t_list_day, t_list_night, mm_day, mm_night

# mm_temp_9_day_forecast("Zīlāni")
# mm_temp_9_day_forecast("Alūksne")


def check_list_len(l):
    """"lvgmc webpage may have incorrect data displayed in some forecasts, this function validates correct lenght
    and prepares data for excel form"""
    if len(l)==9:
        l.append("")
    elif len(l)<9:
        l = [""] * 10
    elif len(l)>9:
        l = [""] * 10
    return l


def mm_temp_forecast_duplicates(station_dict, dupl, tripl):
    """"Modify data by adding duplicate values and empty values to comply with excel structure"""
    stations_day_temp = []
    stations_night_temp = []
    stations_day_mm = []
    stations_night_mm = []
    for key in station_dict:
        print('Getting data for: ', key)
        t_day,t_night, mm_day, mm_night = mm_temp_9_day_forecast(key)
        t_day = check_list_len(t_day)
        t_night = check_list_len(t_night)
        mm_day = check_list_len(mm_day)
        mm_night = check_list_len(mm_night)
        if key in dupl:
            print('Appending 2x data for: ', key,' to comply with excel structure' )
            stations_day_temp.extend(2 * t_day)
            stations_night_temp.extend(2 * t_night)
            stations_day_mm.extend(2 * mm_day)
            stations_night_mm.extend(2 * mm_night)
        elif key in tripl:
            print('Appending 3x data for: ', key, ' to comply with excel structure')
            stations_day_temp.extend(3 * t_day)
            stations_night_temp.extend(3 * t_night)
            stations_day_mm.extend(3 * mm_day)
            stations_night_mm.extend(3 * mm_night)
        else:
            print('Appending data')
            stations_day_temp.extend(t_day)
            stations_night_temp.extend(t_night)
            stations_day_mm.extend(mm_day)
            stations_night_mm.extend(mm_night)
        time.sleep(10)
    return stations_day_temp, stations_night_temp, stations_day_mm, stations_night_mm

def update_forecast_lvgmc(filename):
    wb_obj = openpyxl.load_workbook(filename)
    # Read the forecast sheet t_mm_prognoze
    sheet = wb_obj["t_mm_prognoze"]
    list_day_t, list_night_t, list_day_mm, list_night_mm = mm_temp_forecast_duplicates(station_dict, dupl_st, tripl_st)

    for i in range(3, 353):
        l = i - 3
        cellref_t = sheet.cell(row=i, column=13)     # writing day temp to M column
        cellref_t.value = list_day_t[l]
        cellref_t = sheet.cell(row=i, column=14)     # writing night temp to N column
        cellref_t.value = list_night_t[l]
        cellref_t = sheet.cell(row=i, column=15)     # writing day mm to O column
        cellref_t.value = list_day_mm[l]
        cellref_t = sheet.cell(row=i, column=16)     # writing night mm to P column
        cellref_t.value = list_night_mm[l]


    wb_obj.save(filename)


update_forecast_lvgmc(completename)
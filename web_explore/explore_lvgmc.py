"""For development - to explore https://videscentrs.lvgmc.lv/ weather feature - temp & rain extraction """
import requests
from datetime import date
import json

today = date.today()
print(today.strftime('%Y%m%d'))


# Send a GET request to gather weather forecast JSON file
def get_station_forecast(url):
    response = requests.get(url)
    data = response.json()
    return data


# Extract temperatura and nokrisni_12h values from JSON file
def explore_weather_json(data):
    for entry in data:
        laiks = entry.get("laiks")
        temperatura = entry.get("temperatura")
        nokrisni_12h = entry.get("nokrisni_12h")
        print(f"{laiks} Temperature: {temperatura}°C, Precipitation (12h): {nokrisni_12h}mm")


# test example for single station
url = "https://videscentrs.lvgmc.lv/data/weather_forecast_for_location_daily?punkts=P3"
test_data = get_station_forecast(url)
print(test_data)
explore_weather_json(test_data)


# station dict with extracted point values, note Lielpeči = Ogre, Sīļi = Silajāni, Vičaki = Ventspils
station_dict = {'Ainaži': 'P3', 'Alūksne':'P14', 'Bauska': 'P67', 'Daugavpils': 'P75', 'Dobele': 'P54',
                'Gulbene': 'P23', 'Jelgava': 'P52', 'Kalnciems': 'P43', 'Kolka': 'P769', 'Kuldīga': 'P31',
                'Lielpeči': 'P42', 'Liepāja': 'P77', 'Mērsrags': 'P729', 'Pāvilosta': 'P36', 'Piedruja': 'P2388',
                'Rēzekne': 'P62', 'Rīga': 'P28', 'Rūjiena': 'P1', 'Saldus': 'P51', 'Sigulda': 'P24', 'Sīļi': 'P2294',
                'Skrīveri': 'P911', 'Stende': 'P26', 'Vičaki': 'P13','Zīlāni': 'P226','Zosēni': 'P2017'}


def test_urls(st_dict):
    for station_name, station_point in st_dict.items():
        url = f"https://videscentrs.lvgmc.lv/data/weather_forecast_for_location_daily?punkts={station_point}"
        print(url)
        response = requests.get(url)
        data = response.json()
        print(data)


test_urls(station_dict)


# Initialize lists for day and night temperatures
day_temperatures = []
night_temperatures = []
day_mm = []
night_mm = []

# Iterate through the data
for entry in test_data[1:]:     # skip first entry (today)
    if entry["laiks"].endswith("1200"):
        day_temperatures.append(float(entry["temperatura"]))
        day_mm.append(float(entry["nokrisni_12h"]))
    elif entry["laiks"].endswith("0000"):
        night_temperatures.append(float(entry["temperatura"]))
        night_mm.append(float(entry["nokrisni_12h"]))

# Print the results
print("Day Temperatures:", day_temperatures)
print("Night Temperatures:", night_temperatures)
print("Day mm:", day_mm)
print("Night mm:", night_mm)





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



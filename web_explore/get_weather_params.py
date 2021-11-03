"""For development - to acquire parameters for script"""
from datetime import date, timedelta
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

help(BeautifulSoup)

# get dates for requests
today = date.today().strftime('%d.%m.%Y')
yesterday = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')  # datums līdz
week_ago = (date.today() - timedelta(days=7)).strftime('%d.%m.%Y')  # datums no

print(yesterday)
print(week_ago)



# get params for requests
url = "https://new.meteo.lv/meteorologija-datu-meklesana/?nid=461"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')

# get values for Gaisa temperatūra, faktiskā & Nokrišņu daudzums, stundas summa

param_temp = soup.find("option", text='Gaisa temperatūra, faktiskā')
param_rain = soup.find("option", text='Nokrišņu daudzums, stundas summa')
print('Value for temp option ', param_temp['value'])
print('Value for rain option ', param_rain['value'])



# getplaces for requests

# Give the location of the excel file
loc = ("data/RU05_laika_apstakli_fakts_prognoze_08042021.xlsx")

# read t_fakts sheet
df_t_fakts = pd.read_excel(loc, sheet_name='t_fakts', skiprows=[0])
# print(df_t_fakts)

stations_list = df_t_fakts['Stacija'].values.tolist()
stations_list = list(dict.fromkeys(stations_list))  # remove duplicate values
print(stations_list)

sample_stations = ['Ainaži', 'Alūksne', 'Bauska', 'Daugavpils', 'Dobele', 'Gulbene', 'Jelgava', 'Kalnciems', 'Kolka', 'Kuldīga', 'Lielpeči', 'Liepāja', 'Mērsrags', 'Pāvilosta', 'Piedruja', 'Rēzekne', 'Rīga', 'Rūjiena', 'Saldus', 'Sigulda', 'Sīļi', 'Skrīveri', 'Stende', 'Vičaki', 'Zīlāni', 'Zosēni']
print(len(sample_stations))
station_dict = {'Ainaži': 30000, 'Alūksne': 30004, 'Bauska': 30011, 'Daugavpils': 30021, 'Dobele': 30022, 'Gulbene': 30034, 'Jelgava': 30036, 'Kalnciems': 30040, 'Kolka': 30046, 'Kuldīga': 30048, 'Lielpeči': 30058, 'Liepāja': 30060, 'Mērsrags': 30072, 'Pāvilosta': 30080, 'Piedruja': 30081, 'Rēzekne': 10000180, 'Rīga': 30096, 'Rūjiena': 30100, 'Saldus': 30102, 'Sigulda': 30103, 'Sīļi': 30104, 'Skrīveri': 30105, 'Stende': 30111, 'Vičaki': 30132, 'Zīlāni': 30140, 'Zosēni': 30141}

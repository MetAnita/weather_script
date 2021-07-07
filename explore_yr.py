"""For development - to explore https://www.yr.no/ weather feature - temp & rain extraction """
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
# url example
# https://www.yr.no/en/forecast/daily-table/2-453822/Latvia/Jaunpiebalga/Zosēnu%20pagasts/Zosēni


# station_dict = {'Ainaži': 'Salacgrīvas/Ainaži/Ainaži', 'Alūksne':'Aluksnes/Alūksne/Alūksne', 'Bauska': 'Bauskas%20Rajons/Bauska/Bauska', 'Daugavpils': 'Daugavpils%20municipality/Daugavpils', 'Dobele': 'Dobeles/Dobele/Dobele', 'Gulbene': 'Gulbenes/Gulbene/Gulbene', 'Jelgava': 'Jelgava/Jelgava/Jelgava', 'Kalnciems': 'Jelgava%20fylke/Kalnciema%20pagasts/Kalnciems', 'Kolka': 'Dundaga/Kolkas%20pagasts/Kolka', 'Kuldīga': 'Kuldigas/Kuldīga/Kuldīga', 'Lielpeči': 'Ogre/Ogre/Ogre', 'Liepāja': 'Liepaja', 'Mērsrags': 'Mesraga/Mērsraga%20novads/Mērsrags', 'Pāvilosta': 'Pāvilostas/Pāvilosta/Pāvilosta', 'Piedruja': 'Daugavpils%20municipality/Piedruja', 'Rēzekne': 'Rezekne/Rēzekne/Rēzekne', 'Rīga': 'Riga/Rīga/Riga', 'Rūjiena': 'Rūjienas/Rūjiena/Rūjiena', 'Saldus': 'Saldus%20Rajons/Saldus/Saldus', 'Sigulda': 'Sigulda/Sigulda/Sigulda', 'Sīļi': 'Preilu/Silajāni', 'Skrīveri': 'Skrīveri/Skrīveru%20novads/Skrīveri', 'Stende': 'Talsi%20Municipality/Stende/Stende', 'Vičaki': 'Ventspils%20Rajons/Ances%20pagasts/Vičaki','Zīlāni': 'Jēkabpils%20Municipality/Zilāni','Zosēni': 'Jaunpiebalga/Zosēnu%20pagasts/Zosēni'}
station_dict = {'Ainaži': '2-461628', 'Alūksne':'2-461528', 'Bauska': '2-461114', 'Daugavpils': '2-460413', 'Dobele': '2-460312', 'Gulbene': '2-459668', 'Jelgava': '2-459279', 'Kalnciems': '2-459102', 'Kolka': '2-458682', 'Kuldīga': '2-458460', 'Lielpeči': '2-457065', 'Liepāja': '5-2640600', 'Mērsrags': '2-457408', 'Pāvilosta': '2-456827', 'Piedruja': '2-456742', 'Rēzekne': '2-456202', 'Rīga': '2-456172', 'Rūjiena': '2-456008', 'Saldus': '2-455890', 'Sigulda': '2-455718', 'Sīļi': '2-455697', 'Skrīveri': '2-455523', 'Stende': '2-455260', 'Vičaki': '2-454251','Zīlāni': '2-453862','Zosēni': '2-453822'}


sample_dict = {'Ainaži': 'Salacgrīvas/Ainaži/Ainaži', 'Alūksne':'Aluksnes/Alūksne/Alūksne', 'Bauska': 'Bauskas%20Rajons/Bauska/Bauska','Zīlāni': 'Jēkabpils%20Municipality/Zilāni' }

# Nokrišņu daudzums, mm
# <span class="precipitation precipitation--hidden precipitation--color" role="text"><span class="nrk-sr">Precipitation </span><span class="precipitation__value">0</span><abbr class="precipitation__unit" title="millimeters">mm</abbr></span>


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
# # print(soup.prettify())
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
mm = soup.find_all('span', {"class":"precipitation__value"})
#
# print('test the temperature - calculate avg')
# for min_temp, max_temp in zip(res_min[1:], res_max[1:]):
#     #sākas ar šodienu
#     min_t = min_temp.contents[0]
#     max_t = max_temp.contents[0]
#     avg_temp = (int(min_t) + int(max_t))/2
#     # print(avg_temp)
#     print(min_temp.contents[0], int(min_temp.contents[0]),  max_temp.contents[0], int(max_temp.contents[0]))
#
print('test the precipitation mm')

# for m in mm:
#     print(m)
#     m_value = m.text
#     print(m_value)

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

    res_max = soup.find_all('span', ["temperature min-max-temperature__max temperature--warm"])
    res_min = soup.find_all('span', ["temperature min-max-temperature__min temperature--warm"])
    res_mm = soup.find_all('span', ["precipitation__value"])

    for m in res_mm[2:]:
        m_value = m.text
        m_value = float(m_value.replace(',', '.'))  # to convert string to float
        mm.append(float(m_value))

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
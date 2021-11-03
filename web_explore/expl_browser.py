"""For development - to explore meteo.lv file download"""
import mechanicalsoup
from datetime import date, timedelta
import os

yesterday = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')  # datums līdz
week_ago = (date.today() - timedelta(days=7)).strftime('%d.%m.%Y')  # datums no
station = 'Alūksne'

# create_request
browser = mechanicalsoup.StatefulBrowser()
browser.open("https://new.meteo.lv/meteorologija-datu-meklesana/")
browser.select_form('form[action="/meteorologija-datu-meklesana/?"]')
# Fill web form
browser["iBy"] = "station"
browser["iStation"] = "30004"
browser["iParameter"] = ("4001", "4570")
# browser["iParameter"] = "4570"
browser["iDateFrom"] = week_ago
browser["iDateTill"] = yesterday

# browser.form.print_summary()
# browser.launch_browser()
response = browser.submit_selected()

# create changeable file name
save_path = '/data'  # SHOULD CHANGE
filename = "abi_%s%s.xls" % (yesterday, station)
completename = os.path.join(save_path, filename)
output = open(completename, 'wb')
output.write(response.content)
output.close()

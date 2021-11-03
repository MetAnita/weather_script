import os
from pathlib import Path
from datetime import date, timedelta

# results file name and location
yesterday = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')  # datums līdz
week_ago = (date.today() - timedelta(days=7)).strftime('%d.%m.%Y')
result_folder_path = Path('results')
xlsx_filename = "laika_apstakli_fakts_prognoze_%s.xlsx" % date.today().strftime('%d%m%Y')
# final_wb = openpyxl.load_workbook('sample_excel.xlsx') # TODO add inside function as var
completename = os.path.join(result_folder_path, xlsx_filename)

# historical weather excel file data folder
station_history = Path('data', date.today().strftime('%Y%m%d'))

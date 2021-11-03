''''Write historical mm and t data from meteo to excel file'''
from pathlib import Path
import openpyxl
import xlrd
from write_info import completename, station_history

station_dict = {'Ainaži': 'ainazi-47075', 'Alūksne': 'aluksne-4124', 'Bauska': 'bauska-4139', 'Daugavpils': 'daugavpils-4177', 'Dobele': 'dobele-4137', 'Gulbene': 'gulbene-4125', 'Jelgava': 'jelgava-4138', 'Kalnciems': 'kalnciems-322319', 'Kolka': 'kolka-47057', 'Kuldīga': 'kuldiga-4106', 'Lielpeči': 'ogre-47066', 'Liepāja': 'liepaja-4134', 'Mērsrags': 'mersrags-47065', 'Pāvilosta': 'pavilosta-47067', 'Piedruja': 'piedruja-322361', 'Rēzekne': 'rezekne-4140', 'Rīga': 'riga-4136', 'Rūjiena': 'rujiena-47073', 'Saldus': 'saldus-4135', 'Sigulda': 'sigulda-4103', 'Sīļi': 'silajani-322513', 'Skrīveri': 'skriveri-322563', 'Stende': 'stende-47083', 'Vičaki': 'ventspils-4123', 'Zīlāni': 'zilani-322369', 'Zosēni': 'vecpiebalga-322623'}
final_wb = openpyxl.load_workbook(completename)
final_t_sheet = final_wb['t_fakts']


# find station row in excel final file
def find_start_row(station):
    row_idx = False
    for row in final_t_sheet.iter_rows(min_col=2, max_col=2):   # B column in Excel file
        for cell in row:
            if cell.value == station:
                # print('Row number:', row[0].row)
                row_idx = row[0].row
    return row_idx


# write temp & rain history for one station in big excel file
def write_t_mm_history(src_filepath, dest_filepath, station):
    station_wb = xlrd.open_workbook(src_filepath)
    final_wb = openpyxl.load_workbook(dest_filepath)
    t_ws = station_wb.sheet_by_name('1. tabula')
    mm_ws = station_wb.sheet_by_name('2. tabula')
    final_t_ws = final_wb['t_fakts']
    final_mm_ws = final_wb['mm_fakts']
    # find station row?
    str_row = find_start_row(station)   # TODO - wrap around try except - for cases when station not found in excel wb
    print(str_row)
    # write temperature
    write_data_chunk(str_row, t_ws, final_t_ws)
    write_data_chunk(str_row, mm_ws, final_mm_ws)
    final_wb.save(dest_filepath)


def write_data_chunk(st_row, src_ws, dest_ws):
    h = 2
    for i in range(st_row, st_row+7):  # destination excel rows from - to
        # get each row from source file into list
        header = src_ws.row_values(h, start_colx=0, end_colx=None)
        print(header)
        h += 1
        if st_row == 3:  # write dates & data for first station     # TODO create different for loop without if statement - for element in a_list[1:]: print(element)
            for j in range(4, 29):  # columns (with date column)
                # reading cell value from source excel file
                c = header[j - 4]
                # writing the read value to destination excel file
                dest_ws.cell(row=i, column=j).value = c
        else:
            for j in range(5, 29):  # columns (without date column)
                # reading cell value from source excel file
                c = header[j - 4]
                # writing the read value to destination excel file
                dest_ws.cell(row=i, column=j).value = c


for key in station_dict:
    print(key)
    st_path = Path(station_history, '%s.xls' % key)
    write_t_mm_history(st_path, completename, key)

#TODO check that excel source data file has all rows
import openpyxl
from pathlib import Path
from write_info import completename, station_history

station_dict = {
    'Ainaži': 'ainazi-47075', 'Alūksne': 'aluksne-4124', 'Bauska': 'bauska-4139',
    'Daugavpils': 'daugavpils-4177', 'Dobele': 'dobele-4137', 'Gulbene': 'gulbene-4125',
    'Jelgava': 'jelgava-4138', 'Kalnciems': 'kalnciems-322319', 'Kolka': 'kolka-47057',
    'Kuldīga': 'kuldiga-4106', 'Lielpeči': 'ogre-47066', 'Liepāja': 'liepaja-4134',
    'Mērsrags': 'mersrags-47065', 'Pāvilosta': 'pavilosta-47067', 'Piedruja': 'piedruja-322361',
    'Rēzekne': 'rezekne-4140', 'Rīga': 'riga-4136', 'Rūjiena': 'rujiena-47073',
    'Saldus': 'saldus-4135', 'Sigulda': 'sigulda-4103', 'Sīļi': 'silajani-322513',
    'Skrīveri': 'skriveri-322563', 'Stende': 'stende-47083', 'Vičaki': 'ventspils-4123',
    'Zīlāni': 'zilani-322369', 'Zosēni': 'vecpiebalga-322623'
}

final_wb = openpyxl.load_workbook(completename)
final_t_sheet = final_wb['t_fakts']


def find_start_row(station, sheet):
    """Find the row in the final sheet where data for the given station should be written."""
    for row in sheet.iter_rows(min_col=2, max_col=2):
        for cell in row:
            if cell.value == station:
                return cell.row
    return None


def write_data_chunk(start_row, src_ws, dest_ws, include_dates=True):
    """Write a chunk of data from the source worksheet to the destination worksheet."""
    for i in range(7):  # 7 rows per station
        header = [cell.value for cell in src_ws[i + 4]]  # Adjust row index as needed
        print(f"Writing data for row {start_row + i}: {header}")

        start_col = 4 if include_dates else 5
        for j in range(start_col, 29):
            dest_ws.cell(row=start_row + i, column=j).value = header[j - 4]


def write_history(src_filepath, dest_filepath, station, sheet_name):
    """Write temperature or mm history from the source to the destination workbook."""
    station_wb = openpyxl.load_workbook(src_filepath)
    final_wb = openpyxl.load_workbook(dest_filepath)

    src_ws = station_wb.worksheets[0]
    dest_ws = final_wb[sheet_name]

    start_row = find_start_row(station, dest_ws)
    if start_row is not None:
        include_dates = start_row == 3
        write_data_chunk(start_row, src_ws, dest_ws, include_dates)
        final_wb.save(dest_filepath)
    else:
        print(f"Start row not found for station: {station}")


# Process temperature and mm data for each station
for station in station_dict:
    print(f"Processing data for: {station}")

    # Write temperature data
    temp_filepath = Path(station_history, f'{station}_temp.xlsx')
    write_history(temp_filepath, completename, station, 't_fakts')

    # Write mm data
    mm_filepath = Path(station_history, f'{station}_mm.xlsx')
    write_history(mm_filepath, completename, station, 'mm_fakts')

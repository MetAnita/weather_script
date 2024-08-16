from datetime import date, timedelta
from pathlib import Path
import time
import requests
from urllib.error import HTTPError
from write_info import create_results_file, sample_xlsx


# Constants
BASE_URL = (
    "https://videscentrs.lvgmc.lv/media/reports/station-report.xls"
    "?format=xls&mode=meteo&sakuma_datums={day_from}&beigu_datums={day_to}"
    "&stacija_id={station}&raditaja_id={param}"
)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
RETRY_DELAY = 5
DOS_DELAY = 6


def create_folder():
    """Create a directory for saving files based on the current date."""
    folder = Path('data', date.today().strftime('%Y%m%d'))
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_dates():
    """Return today, yesterday, and a week ago in the correct format."""
    today = date.today()
    return today.strftime('%Y-%m-%d'), (today - timedelta(days=1)).strftime('%Y-%m-%d'), (today - timedelta(days=7)).strftime('%Y-%m-%d')


def download_file(url, save_path):
    """Download a file from the given URL and save it to the specified path."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the file: {e}")
        raise


def read_weather_history(station, day_from, day_to, param1, param2, station_name, folder_path):
    """Download weather history for two parameters and save as separate files."""
    for param, suffix in [(param1, "temp"), (param2, "mm")]:
        url = BASE_URL.format(day_from=day_from, day_to=day_to, station=station, param=param)
        filename = f"{station_name}_{suffix}.xlsx"
        save_path = folder_path / filename
        print(f"Attempting to download {filename}...")
        download_file(url, save_path)


def main():
    folder_path = create_folder()
    today, yesterday, week_ago = get_dates()

    create_results_file(sample_xlsx)

    station_dict = {
        'Ainaži': 30000, 'Alūksne': 30004, 'Bauska': 30011, 'Daugavpils': 30021, 'Dobele': 30022, 'Gulbene': 30034,
        'Jelgava': 30036, 'Kalnciems': 30040, 'Kolka': 30046, 'Kuldīga': 30048, 'Lielpeči': 30058, 'Liepāja': 30060,
        'Mērsrags': 30072, 'Pāvilosta': 30080, 'Piedruja': 30081, 'Rēzekne': 10000180, 'Rīga': 30096, 'Rūjiena': 30100,
        'Saldus': 30102, 'Sigulda': 30103, 'Sīļi': 30104, 'Skrīveri': 30105, 'Stende': 30111, 'Vičaki': 30132,
        'Zīlāni': 30140, 'Zosēni': 30141
    }

    for station_name, station_id in station_dict.items():
        print(f"Processing station: {station_name} ({station_id})")
        time.sleep(DOS_DELAY)
        while True:
            try:
                read_weather_history(str(station_id), week_ago, yesterday, "4001", "4570", station_name, folder_path)
                break
            except HTTPError:
                print("Server error, retrying...")
                time.sleep(RETRY_DELAY)
                continue


if __name__ == "__main__":
    main()

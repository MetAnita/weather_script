from datetime import date, timedelta
from pathlib import Path
import time
import requests
from urllib.error import HTTPError
from write_info import create_results_file, sample_xlsx, station_dict

# Constants
BASE_URL = "https://videscentrs.lvgmc.lv/noverojumu-arhivs/meteo/{station}/active/{param}/{day_from}/{day_to}"

# Constants
POST_URL = "https://videscentrs.lvgmc.lv/data/na_prepare"
BASE_DOWNLOAD_URL = "https://videscentrs.lvgmc.lv/media/reports/arhivs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Content-Type": "application/json",
}
RETRY_DELAY = 5
DOS_DELAY = 5


def create_folder():
    """Create a directory for saving files based on the current date."""
    folder = Path('data', date.today().strftime('%Y%m%d'))
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_dates():
    """Return today, yesterday, and a week ago in the correct format."""
    today = date.today()
    return today.strftime('%Y-%m-%d'), (today - timedelta(days=1)).strftime('%Y-%m-%d'), (today - timedelta(days=7)).strftime('%Y-%m-%d')


def generate_report(station_id, param, start_date, end_date):
    """
    Send a POST request to generate a weather report.

    Returns:
        int: The report ID from the server response.
    """
    payload = {
        "stacija_id": station_id,
        "mode": "meteo",
        "raditaja_id": param,
        "sakuma_laiks": start_date,
        "beigu_laiks": end_date,
    }

    response = requests.post(POST_URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    response_data = response.json()
    report_id = response_data.get("id")

    if report_id is None:
        raise ValueError("Failed to generate report: Missing 'id' in response.")

    return report_id


def download_report(report_id, station_name,  suffix, folder_path):
    """
    Download the report using the generated report ID.

    """
    filename = f"{station_name}_{suffix}.xlsx"
    download_url = f"{BASE_DOWNLOAD_URL}/{filename}?id={report_id}"

    # Attempt to download the file
    try:
        print(f"Fetching report: {download_url}")
        response = requests.get(download_url, headers=HEADERS)
        response.raise_for_status()

        save_path = folder_path / filename
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Report saved to: {save_path}")
    except requests.RequestException as e:
        print(f"Failed to download the report: {e}")
        raise


def read_weather_history(station_id, start_date, end_date, param1, param2, station_name, folder_path):
    """
    Generate and download weather reports for two parameters.

    Args:
        station_id (int): The station ID.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        param1 (int): First parameter ID (e.g., temperature).
        param2 (int): Second parameter ID (e.g., precipitation).
        station_name (str): The name of the station.
        folder_path (Path): Folder to save the files.

    """
    for param, suffix in [(param1, "temp"), (param2, "mm")]:
        try:
            print(f"Generating report for {station_name} ({suffix})...")
            report_id = generate_report(station_id, param, start_date, end_date)
            time.sleep(DOS_DELAY)
            download_report(report_id, station_name, suffix, folder_path)
        except Exception as e:
            print(f"Error processing {station_name} ({suffix}): {e}")


def main():
    folder_path = create_folder()
    today, yesterday, week_ago = get_dates()

    create_results_file(sample_xlsx)

    for station_name, station_id in station_dict.items():
        print(f"Processing station: {station_name}")
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

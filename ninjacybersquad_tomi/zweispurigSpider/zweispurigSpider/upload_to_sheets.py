import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import glob
import os

def upload_to_sheets(json_folder_path, sheet_name):
    # Find the most recent JSON file
    list_of_files = glob.glob(os.path.join(json_folder_path, '*.json'))
    latest_file = max(list_of_files, key=os.path.getctime)

    # Global Google Sheet API Settings
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('spidersheet.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    sheet.clear()

    # Load data from the most recent JSON file
    with open(latest_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if data is not empty and has items
    if data:
        headers = list(data[0].keys())
        # Upload headers
        sheet.append_row(headers)
        for item in data:
            row = list(item.values())
            # Upload each item
            sheet.append_row(row)

if __name__ == "__main__":
    json_folder_path = os.path.join('backup', 'crawlerjson')
    credentials_file = 'spidersheet.json'  # Path to your credentials file
    upload_to_sheets(json_folder_path, 'ZweispurigSpider', credentials_file)

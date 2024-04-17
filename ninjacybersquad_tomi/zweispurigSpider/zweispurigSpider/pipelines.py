import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import pandas as pd

class GoogleSheetsAndJsonPipeline:
    def __init__(self):
        self.overwrite_headers = True

    def open_spider(self, spider):
        backup_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'backup', 'crawlerjson')  # Go back one folder, into backup, then into crawlerjson
        os.makedirs(backup_folder, exist_ok=True)  # Ensure the backup folder exists
        timestamp = time.strftime("%Y%m%d")  # Get current date as a timestamp
        filename = f"{timestamp}_crawled.json"  # Create filename with timestamp
        self.file_path = os.path.join(backup_folder, filename)  # Construct file path
        self.file = open(self.file_path, 'w', encoding='utf-8')  # Open file for writing

        # Google Sheets setup
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        json_file_path = os.path.join(os.path.dirname(__file__), 'spidersheet.json')  # Assuming spidersheet.json is in the same folder as this script
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open('ZweispurigSpider').sheet1

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

        timestamp = time.strftime("%Y%m%d")

        # Read the file content, split by lines, and filter out empty lines
        with open(self.file_path, 'r', encoding='utf-8') as json_file:
            lines = [line for line in json_file if line.strip()]
            file_content = ",".join(lines)
            # Wrap with brackets to form a valid JSON array
            data = json.loads(f"[{file_content}]")  

        # Convert JSON data to DataFrame
        df = pd.DataFrame(data)

        # Create Excel filename with timestamp
        excel_filename = f"{timestamp}_crawled.xlsx"

        # Construct Excel file path
        excel_file_path = os.path.join(os.path.dirname(self.file_path), '..', '..', 'backup', 'crawlerexcel', excel_filename)

        # Write DataFrame to Excel
        df.to_excel(excel_file_path, index=False)

        # Clear the sheet before if boolean true
        if self.overwrite_headers and data:
            self.sheet.clear() 
            headers = list(data[0].keys())
            # Append the headers as the first row in the sheet
            self.sheet.append_row(headers)  

            # Batch upload data to the sheet (this and time.sleep to avoid hitting Google Sheets API rate limits)
            batch_size = 100
            for i in range(0, len(data), batch_size):
                batch = [list(item.values()) for item in data[i:i+batch_size]]
                self.sheet.append_rows(batch) 
                time.sleep(1)

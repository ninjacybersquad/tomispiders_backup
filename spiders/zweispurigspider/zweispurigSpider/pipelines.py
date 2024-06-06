import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import pandas as pd

class GoogleSheetsAndJsonPipeline:
    def __init__(self, upload_enabled=False):
        self.overwrite_headers = True
        self.upload_enabled = upload_enabled  # Control uploading to Google Sheets

    def open_spider(self, spider):
        backup_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'backup', 'crawlerjson')
        os.makedirs(backup_folder, exist_ok=True)
        timestamp = time.strftime("%Y%m%d")
        filename = f"{timestamp}_crawled.json"
        self.file_path = os.path.join(backup_folder, filename)
        self.file = open(self.file_path, 'w', encoding='utf-8')

        # Google Sheets setup only if upload is enabled
        if self.upload_enabled:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            json_file_path = os.path.join(os.path.dirname(__file__), 'spidersheet.json')
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
        with open(self.file_path, 'r', encoding='utf-8') as json_file:
            lines = [line for line in json_file if line.strip()]
            file_content = ",".join(lines)
            data = json.loads(f"[{file_content}]")
        df = pd.DataFrame(data)
        excel_filename = f"{timestamp}_crawled.xlsx"
        excel_file_path = os.path.join(os.path.dirname(self.file_path), '..', '..', 'backup', 'crawlerexcel', excel_filename)
        df.to_excel(excel_file_path, index=False)

        # Perform Google Sheets operations only if upload is enabled
        if self.upload_enabled and data:
            self.sheet.clear()
            headers = list(data[0].keys())
            self.sheet.append_row(headers)
            batch_size = 100
            for i in range(0, len(data), batch_size):
                batch = [list(item.values()) for item in data[i:i+batch_size]]
                self.sheet.append_rows(batch)
                time.sleep(1)

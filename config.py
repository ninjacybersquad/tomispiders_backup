# config.py
from datetime import datetime
import os

# Function to create a directory if it doesn't exist
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Date stamp for file naming
date_stamp = datetime.now().strftime("%d%m%Y")

# Log Paths
logs_base_path = 'backup/logs'
create_dir(logs_base_path)
log_filename = f"{date_stamp}_log.txt"
log_filepath = os.path.join(logs_base_path, log_filename)

# Crawled Data Paths
crawled_json_path = 'backup/crawlerjson'
crawled_excel_path = 'backup/crawlerexcel'
create_dir(crawled_json_path)
create_dir(crawled_excel_path)
crawled_json_filename = f"{date_stamp}_crawled.json"
crawled_excel_filename = f"{date_stamp}_crawled.xlsx"
crawled_json_fullpath = os.path.join(crawled_json_path, crawled_json_filename)
crawled_excel_fullpath = os.path.join(crawled_excel_path, crawled_excel_filename)

# Reference File Path for Comparison
reference_file_path = 'backup/willhaben/willhaben.xlsx'
create_dir(os.path.dirname(reference_file_path))

# Matched Data Paths
matched_json_path = 'backup/matchedjson'
matched_excel_path = 'backup/matchedexcel'
create_dir(matched_json_path)
create_dir(matched_excel_path)

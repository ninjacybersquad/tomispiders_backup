import subprocess
from datetime import datetime
import pandas as pd
import os
import sys

# Import the compare functions
from scripts.compare_data import main as compare_main

# --- Path Configurations ---

# Date stamp for file naming
date_stamp = datetime.now().strftime("%d%m%Y")

# Log Paths
logs_base_path = 'logs'
if not os.path.exists(logs_base_path):
    os.makedirs(logs_base_path)
log_filename = f"{date_stamp}_log.txt"
log_filepath = os.path.join(logs_base_path, log_filename)

# Print a message to the console indicating the process will take a while
print("Starting the data crawling and conversion process. This might take a while...")

# Overwrite the log file if it exists
log_file = open(log_filepath, 'w')
sys.stdout = log_file
sys.stderr = log_file

# Crawled Data Paths
crawled_base_path = 'data/crawled'
crawled_json_path = f"{crawled_base_path}/json"
crawled_excel_path = f"{crawled_base_path}/excel"
crawled_json_filename = f"{date_stamp}_crawled.json"
crawled_excel_filename = f"{date_stamp}_crawled.xlsx"
crawled_json_fullpath = f"{crawled_json_path}/{crawled_json_filename}"
crawled_excel_fullpath = f"{crawled_excel_path}/{crawled_excel_filename}"

# Reference File Path for Comparison
reference_file_path = 'data/willhaben/willhaben.xlsx'

# Matched Data Paths
matched_base_path = 'data/matched'
matched_json_path = f"{matched_base_path}/json"
matched_excel_path = f"{matched_base_path}/excel"

# Function to run the spider and save crawled data directly to JSON
def run_spider():
    try:
        if os.path.exists(crawled_json_fullpath):
            os.remove(crawled_json_fullpath)
            print(f"Existing JSON file removed. Preparing to create a new file: {crawled_json_fullpath}")

        print(f"Running spider and saving output to: {crawled_json_fullpath}")
        result = subprocess.run(
            ['scrapy', 'crawl', 'zweispurig', '-o', f'../../{crawled_json_fullpath}'],
            cwd='./spiders/zweispurigspider',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
        print("Spider run completed successfully.")
    except Exception as e:
        print(f"An error occurred while running the spider: {e}")


# Function to convert the JSON data to an Excel file
def convert_json_to_excel():
    try:
        if os.path.exists(crawled_excel_fullpath):
            os.remove(crawled_excel_fullpath)
            print(f"Existing Excel file removed. Preparing to create a new file: {crawled_excel_fullpath}")

        if not os.path.exists(crawled_json_fullpath):
            print(f"Error: JSON file not found at {crawled_json_fullpath}")
            return
        else:
            print(f"JSON file found at: {crawled_json_fullpath}")
            with open(crawled_json_fullpath, 'r') as file:
                print("Inspecting the first 500 characters of the JSON file content:")
                print(file.read(500))

            print(f"Reading JSON data from: {crawled_json_fullpath}")
            data = pd.read_json(crawled_json_fullpath)

            print(f"Converting JSON data to Excel and saving to: {crawled_excel_fullpath}")
            data.to_excel(crawled_excel_fullpath, index=False, engine='openpyxl')
            print(f"Data successfully converted to Excel and saved to: {crawled_excel_fullpath}")
    except Exception as e:
        print(f"An error occurred while converting JSON to Excel: {e}")


# Function to run the comparison between the crawled Excel data and the reference file
def run_comparison(crawled_excel_fullpath, reference_file_path):
    try:
        print(f"Running comparison between {crawled_excel_fullpath} and {reference_file_path}")
        matched_df = compare_main(crawled_excel_fullpath, reference_file_path)
        if matched_df is not None:
            print("Comparison completed successfully.")
            save_matched_data(matched_df)
        else:
            print("Comparison failed or returned no results.")
    except Exception as e:
        print(f"An error occurred during the comparison: {e}")


# Function to save the matched data to JSON and Excel
def save_matched_data(matched_df):
    try:
        if not os.path.exists(matched_json_path):
            os.makedirs(matched_json_path)
        if not os.path.exists(matched_excel_path):
            os.makedirs(matched_excel_path)

        matched_json_filename = f"{date_stamp}_matched.json"
        matched_excel_filename = f"{date_stamp}_matched.xlsx"
        matched_json_fullpath = f"{matched_json_path}/{matched_json_filename}"
        matched_excel_fullpath = f"{matched_excel_path}/{matched_excel_filename}"

        print(f"Saving matched data to JSON file: {matched_json_fullpath}")
        matched_df.to_json(matched_json_fullpath, orient='records', lines=True)

        print(f"Saving matched data to Excel file: {matched_excel_fullpath}")
        matched_df.to_excel(matched_excel_fullpath, index=False, engine='openpyxl')
        print("Matched data successfully saved.")
    except Exception as e:
        print(f"An error occurred while saving matched data: {e}")


if __name__ == '__main__':
    try:
        run_spider()
    except Exception as e:
        print(f"An error occurred in run_spider: {e}")

    try:
        convert_json_to_excel()
    except Exception as e:
        print(f"An error occurred in convert_json_to_excel: {e}")

    try:
        run_comparison(crawled_excel_fullpath, reference_file_path)
    except Exception as e:
        print(f"An error occurred in run_comparison: {e}")

log_file.close()

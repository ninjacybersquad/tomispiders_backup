import pandas as pd
from fuzzywuzzy import process, fuzz
import os
from datetime import datetime

def find_latest_file_with_date(directory, date_str, file_suffix):
    files = os.listdir(directory)
    files = [file for file in files if file.startswith(date_str) and file.endswith(file_suffix)]
    if files:
        latest_file = sorted(files)[-1]
        print(f"Latest file found: {latest_file}")
        return os.path.join(directory, latest_file)
    else:
        print("No files found for today.")
    return None

def load_data(base_dir):
    today_date = datetime.now().strftime("%Y%m%d")
    print(f"Today's date for file search: {today_date}")
    crawlerexcel_dir = os.path.join(base_dir, 'backup', 'crawlerexcel')
    willhaben_dir = os.path.join(base_dir, 'backup', 'willhaben')
    ninjacybersquad_file = find_latest_file_with_date(crawlerexcel_dir, today_date, '_crawled.xlsx')
    willhaben_file = os.path.join(willhaben_dir, 'willhaben.xlsx')

    if not ninjacybersquad_file or not os.path.exists(willhaben_file):
        print("Required files are missing.")
        exit()  # Exit if files are not found

    print("Loading data from Excel sheets...")
    ninjacybersquad_df = pd.read_excel(ninjacybersquad_file)
    willhaben_df = pd.read_excel(willhaben_file)
    ninjacybersquad_df['match'] = 'No'  # Initialize all entries as 'No' match
    print("Data loaded successfully.")
    return ninjacybersquad_df, willhaben_df

def compare_data(ninjacybersquad_df, willhaben_df):
    name_similarity_threshold = 99
    print("Starting the comparison process...")
    for ninja in ninjacybersquad_df.itertuples():
        exact_matches = willhaben_df[
            (willhaben_df['Adresse 1: PLZ (Firma) (Firma)'].astype(str) == str(ninja.postleitzahl)) &
            (willhaben_df['Adresse 1: Ort (Firma) (Firma)'] == ninja.ort) &
            (willhaben_df['Adresse 1: Anschrift 1 (Firma) (Firma)'] == ninja.street_address)
        ]

        if not exact_matches.empty:
            matched_name = exact_matches.iloc[0]['Firma']
            print(f"Exact match found for {ninja.name} with {matched_name}.")
            ninjacybersquad_df.loc[ninja.Index, 'match'] = exact_matches.iloc[0]['OrgID Auto&Motor (Firma) (Firma)']
        else:
            potential_matches = process.extract(ninja.name, willhaben_df['Firma'], limit=10, scorer=fuzz.token_set_ratio)
            for matched_name, score, idx in potential_matches:
                if score >= name_similarity_threshold:
                    willhaben_row = willhaben_df.iloc[idx]
                    print(f"Found potential match for {ninja.name} with {matched_name} (Score: {score}).")
                    ninjacybersquad_df.loc[ninja.Index, 'match'] = willhaben_row['OrgID Auto&Motor (Firma) (Firma)']
                    break
    return ninjacybersquad_df

def save_data(ninjacybersquad_df, base_dir):
    today_date = datetime.now().strftime("%Y%m%d")
    output_dir_excel = os.path.join(base_dir, 'backup', 'matchedexcel')
    output_dir_json = os.path.join(base_dir, 'backup', 'matchedjson')
    if not os.path.exists(output_dir_excel):
        os.makedirs(output_dir_excel)
    if not os.path.exists(output_dir_json):
        os.makedirs(output_dir_json)

    output_filename_excel = os.path.join(output_dir_excel, f"{today_date}_matched.xlsx")
    output_filename_json = os.path.join(output_dir_json, f"{today_date}_matched.json")
    ninjacybersquad_df.to_excel(output_filename_excel, index=False)
    ninjacybersquad_df.to_json(output_filename_json, orient='records', lines=True)
    print(f"Updated Excel file saved as {output_filename_excel}.")
    print(f"Updated JSON file saved as {output_filename_json}.")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # One level up from the current script directory
    ninjacybersquad_df, willhaben_df = load_data(base_dir)
    ninjacybersquad_df = compare_data(ninjacybersquad_df, willhaben_df)
    save_data(ninjacybersquad_df, base_dir)

if __name__ == '__main__':
    main()

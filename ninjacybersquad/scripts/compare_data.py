import pandas as pd
from fuzzywuzzy import process, fuzz
import os

def load_data(crawled_file_path, reference_file_path):
    if not os.path.exists(crawled_file_path):
        print(f"Error: Crawled file not found at {crawled_file_path}")
        return None, None
    if not os.path.exists(reference_file_path):
        print(f"Error: Reference file not found at {reference_file_path}")
        return None, None

    print("Loading data from Excel sheets...")
    ninjacybersquad_df = pd.read_excel(crawled_file_path)
    willhaben_df = pd.read_excel(reference_file_path)
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

def main(crawled_file_path, reference_file_path):
    ninjacybersquad_df, willhaben_df = load_data(crawled_file_path, reference_file_path)
    if ninjacybersquad_df is not None and willhaben_df is not None:
        matched_df = compare_data(ninjacybersquad_df, willhaben_df)
        return matched_df
    else:
        print("Comparison aborted due to missing data.")
        return None

if __name__ == '__main__':
    # Example usage:
    # crawled_file = 'path/to/crawled_file.xlsx'
    # reference_file = 'path/to/reference_file.xlsx'
    # result_df = main(crawled_file, reference_file)
    pass

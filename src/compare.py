import argparse
import pandas as pd
from datetime import datetime, timedelta

def read_csv(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    return df[['Date', 'Amount']].to_dict(orient='records')

def compare_entries(reference_data, other_data):
    mismatches = []
    reference_set = {(entry['Date'], entry['Amount']) for entry in reference_data}
    other_set = {(entry['Date'], entry['Amount']) for entry in other_data}

    def is_within_date_range(date, amount, data_set):
        date_range = [(date + timedelta(days=i), amount) for i in range(-4, 5)]
        for d in date_range:
            if (d,amount) in data_set:
                return True
        return any((d, amount) in data_set for d in date_range)

    for entry in other_data:
        date = entry['Date']
        amount = entry['Amount']
        if not is_within_date_range(date, amount, reference_set):
            mismatches.append({'entry': entry, 'source': 'other_data'})

    for entry in reference_data:
        date = entry['Date']
        amount = entry['Amount']
        if not is_within_date_range(date, amount, other_set):
            mismatches.append({'entry': entry, 'source': 'reference_data'})

    return mismatches

def main():
    parser = argparse.ArgumentParser(description='Compare two CSV files and find mismatched entries.')
    parser.add_argument('reference_file', type=str, help='Path to the reference CSV file')
    parser.add_argument('other_file', type=str, help='Path to the other CSV file')

    args = parser.parse_args()

    reference_data = read_csv(args.reference_file)
    other_data = read_csv(args.other_file)

    mismatches = compare_entries(reference_data, other_data)

    if mismatches:
        print("Mismatched entries:")
        for mismatch in mismatches:
            print(f"Source: {mismatch['source']}, Entry: {mismatch['entry']}")
    else:
        print("All entries match.")

if __name__ == "__main__":
    main()
import argparse
import csv
from datetime import datetime, timedelta

def read_csv(file_path):
    """Reads a CSV file and returns a list of rows as dictionaries."""
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        for entry in data:
            entry['Date'] = datetime.strptime(entry['Date'], '%m/%d/%Y')
            entry['Amount'] = float(entry['Amount'])
        return data

def compare_entries(reference_data, other_data, show_matches):
    matches = []
    mismatches = []

    for ref_row in reference_data:
        matched = False
        for other_row in other_data:
            date_diff = abs((ref_row['Date'] - other_row['Date']).days)
            if ref_row['Amount'] == other_row['Amount'] and date_diff <= 4:
                matched = True
                matches.append((ref_row, other_row))
                break
        if not matched:
            mismatches.append((ref_row, 'Reference File'))

    for other_row in other_data:
        matched = False
        for ref_row in reference_data:
            date_diff = abs((ref_row['Date'] - other_row['Date']).days)
            if ref_row['Amount'] == other_row['Amount'] and date_diff <= 4:
                matched = True
                break
        if not matched:
            mismatches.append((other_row, 'Other File'))

    if mismatches:
        print("\nMismatched entries:")
        for entry, source in mismatches:
            print(f"Source: {source}, Entry: {entry}")  
    else:
        print("\nNo mismatches found.")

    if show_matches:
        if matches:
            print("\nMatched entries:")
            for ref, other in matches:
                print(f"Reference: {ref}, Other: {other}")
        else:
            print("\nNo matches found.")

    # Calculate and print sum of amounts for each file
    ref_sum = sum(row['Amount'] for row in reference_data)
    cmp_sum = sum(row['Amount'] for row in other_data)
    print(f"\nTotal amount in Reference File: {ref_sum:.2f}")
    print(f"Total amount in Compare File: {cmp_sum:.2f}")
   
def main():
    parser = argparse.ArgumentParser(description='Compare two CSV files and find mismatched entries.')
    parser.add_argument('reference_file', type=str, help='Path to the reference CSV file')
    parser.add_argument('other_file', type=str, help='Path to the other CSV file')
    parser.add_argument('-s', '--show-matches', action='store_true', help='Show matched entries')

    args = parser.parse_args()

    reference_data = read_csv(args.reference_file)
    other_data = read_csv(args.other_file)

    compare_entries(reference_data, other_data, args.show_matches)

    # if mismatches:
    #     print("Mismatched entries:")
    #     for mismatch in mismatches:
    #         print(f"Source: {mismatch['source']}, Entry: {mismatch['entry']}")
    # else:
    #     print("All entries match.")

if __name__ == "__main__":
    main()
#! /usr/bin/env python3
import argparse
import csv
from datetime import datetime, timedelta

def parse_amount(amount):
    """Parses a string into a float."""
    return float(amount.replace('$', '').replace(',', ''))

def get_description_key(entry):
    """ Find possible key for description field in the entry """
    possible_keys = ['Transaction description', 'Payee', 'Name', 'Transaction Detail']
    for key in entry.keys():
        if key in possible_keys or 'description' in key.lower():
            return key
    raise ValueError("Description key not found in the entry")

def read_csv(file_path):
    """Reads a CSV file and returns a list of rows as dictionaries."""
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        for entry in data:
            entry['Date'] = datetime.strptime(entry['Date'], '%m/%d/%Y')
            entry['Amount'] = parse_amount(entry['Amount'])
            entry['Description'] = entry[get_description_key(entry)]
        return data, reader.fieldnames  # Return data and fieldnames

def compare_entries(reference_data, other_data, date_delta = 4):
    matches = []
    mismatches = []
    matched_ref_indices = set()
    matched_other_indices = set()

    for ref_idx,ref_row in enumerate(reference_data):
        matched = False
        for other_idx, other_row in enumerate(other_data):
            if other_idx in matched_other_indices:
                continue
            date_diff = abs((ref_row['Date'] - other_row['Date']).days)
            if ref_row['Amount'] == other_row['Amount'] and date_diff <= date_delta:
                matched = True
                matches.append((ref_row, other_row))
                matched_ref_indices.add(ref_idx)
                matched_other_indices.add(other_idx)
                break
        if not matched:
            mismatches.append((ref_row, 'Reference File'))

    for other_idx, other_row in enumerate(other_data):
        if other_idx in matched_other_indices:
            continue
        matched = False
        for ref_idx, ref_row in enumerate(reference_data):
            if ref_idx in matched_ref_indices:
                continue
            date_diff = abs((ref_row['Date'] - other_row['Date']).days)
            if ref_row['Amount'] == other_row['Amount'] and date_diff <= date_delta:
                matched = True
                break
        if not matched:
            mismatches.append((other_row, 'Other File'))

    return mismatches, matches

def export_mismatches_to_csv(file_path, mismatches, fieldnames):
    if not file_path:
        return

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Source'] + fieldnames)  # Include all fieldnames
        for entry, source in mismatches:
            formatted_date = entry['Date'].strftime('%m/%d/%Y')
            row = [source] + [entry.get(field, '') for field in fieldnames]
            row[fieldnames.index('Date') + 1] = formatted_date  # Update formatted date
            writer.writerow(row)
    print(f"\nMismatches exported to {file_path}")
def export_matches_to_csv(file_path, matches, fieldnames):
    if not file_path:
        return

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ref Date', 'Ref Description', 'Ref Amount', 'Other Date', 'Other Description', 'Other Amount']+fieldnames)  # Include all fieldnames
        for ref, other in matches:
            ref_date = ref['Date'].strftime('%m/%d/%Y')
            other_date = other['Date'].strftime('%m/%d/%Y')
            row = [ref_date, ref['Description'], ref['Amount'], other_date, other['Description'], other['Amount']] \
                    + [ref.get(field, '') for field in fieldnames] \
                    + [other.get(field, '') for field in fieldnames]  # Add other fields
            writer.writerow(row)
    print(f"\nMatches exported to {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Compare two CSV files and find mismatched entries.')
    parser.add_argument('reference_file', type=str, help='Path to the reference CSV file')
    parser.add_argument('other_file', type=str, help='Path to the other CSV file')
    parser.add_argument('-s', '--show-matches', action='store_true', help='Show matched entries')
    parser.add_argument('-d', '--date-delta', type=int, default=4, help='Number of days to consider for date matching')
    parser.add_argument('-o', '--output-file', type=str, help='Path to the output CSV file for mismatches')
    parser.add_argument('-m', '--matches-file', type=str, help='Path to the output CSV file for matches')

    args = parser.parse_args()

    reference_data, reference_fieldnames = read_csv(args.reference_file)
    other_data, other_fieldnames = read_csv(args.other_file)

    # Merge fieldnames
    all_fieldnames = list(set(reference_fieldnames + other_fieldnames))

    mismatches, matches = compare_entries(reference_data, other_data, args.date_delta)

    if mismatches:
        mismatches.sort(key=lambda x: (x[1], x[0]['Date']))
        num_mismatches = len(mismatches)
        print(f"\n There are {num_mismatches} Mismatched entries:")
        print(f"{'Source':<15}{'Date':<12}{'Description':<50}{'Amount':<10}")
        print("-" * 90)
        
        for entry, source in mismatches:
            formatted_date = entry['Date'].strftime('%m/%d/%Y')
            print(f"{source:<15}{formatted_date:<12}{entry['Description']:<50}{entry['Amount']:<10.2f}")

        # Export mismatches to a CSV file
        export_mismatches_to_csv(args.output_file, mismatches, all_fieldnames)
    else:
        print("\nNo mismatches found.")

    if matches:
        if args.show_matches:
    
            print("\nMatched entries:")
            print(f"{'Ref Date':<12}{'Ref Description':<50}{'Ref Amt':<10}{'Other Date':<12}{'Other Description':<50}{'Other Amt':<10}")
            print("-" * 150)
            for ref, other in matches:
                ref_date = ref['Date'].strftime('%m/%d/%Y')
                other_date = other['Date'].strftime('%m/%d/%Y')
                print(f"{ref_date:<12}{ref['Description']:<50}{ref['Amount']:<10.2f}{other_date:<12}{other['Description']:<50}{other['Amount']:<10.2f}")
                #print(f"Reference: {ref}, Other: {other}")
        # Export matches to a CSV file
        export_matches_to_csv(args.matches_file, matches, all_fieldnames)
    else:
        print("\nNo matches found.")

    # Calculate and print sum of amounts for each file
    ref_sum = sum(row['Amount'] for row in reference_data)
    cmp_sum = sum(row['Amount'] for row in other_data)
    print(f"\nTotal amount in Reference File: {ref_sum:.2f}")
    print(f"Total amount in Compare File: {cmp_sum:.2f}")

 
if __name__ == "__main__":
    main()
#! /usr/bin/env python3
import argparse
import csv
import os

## ===== Configuration =====
INPUT_FOLDER = os.path.expanduser('~/Documents/Inbox/CSV/Bank')
OUTPUT_FOLDER = os.path.join(INPUT_FOLDER, 'Filtered')
COLUMNS_TO_KEEP = ['Post Date', 'Transaction Detail','Amount']
# Rename columns for output
COLUMN_RENAME_MAP = {'Post Date': 'Date'}
OUTPUT_COLUMNS = [COLUMN_RENAME_MAP.get(col, col) for col in COLUMNS_TO_KEEP]
def process_csv_file(input_path, output_path):
    try:
        with open(input_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            if not all(col in reader.fieldnames for col in COLUMNS_TO_KEEP):
                print(f"Skipping {os.path.basename(input_path)}: Missing required columns.")
                return
            filtered_rows = []
            for row in reader:
                # Apply COLUMN_RENAME_MAP to the row
                filtered_row = {COLUMN_RENAME_MAP.get(col, col): row[col] for col in COLUMNS_TO_KEEP if col in row}
                filtered_rows.append(filtered_row)

        # Ensure the output file uses renamed columns
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=OUTPUT_COLUMNS)
            writer.writeheader()
            writer.writerows(filtered_rows)

        print(f"Processed {input_path} and saved to {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def main():
    print(f"Scanning folder: {INPUT_FOLDER}")
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith('.csv') and not filename.startswith('Filtered'):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_filename = f"Filtered_{filename}"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            process_csv_file(input_path, output_path)
    print("Processing complete.")
    
if __name__ == "__main__":
    main()
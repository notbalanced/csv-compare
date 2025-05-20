#!/usr/bin/env python3

import csv
import argparse
import os
import sys

# This script filters and renames columns in a CSV file based on a mapping provided in another CSV file.
# The script takes three command-line arguments:
# 1. `-c` or `--columns`: Path to the CSV file containing column mappings.
# 2. `-i` or `--input`: Path to the input CSV file containing the full data.
# 3. `-o` or `--output`: Path to the output CSV file where the filtered data will be saved. 
# If not provided, the output file will be named based on the input file with "_filtered" appended before the extension.
# The script will read the column mappings from the columns file, 
# filter the input CSV based on these mappings, and write the filtered data to the output file.
# The column mappings file should contain two columns: the first for the original column name and the second for the new column name. If the second column is empty, the original name will be used in the output.

def filter_and_rename_columns(data_file, columns_file, output_file):
    if not os.path.isfile(data_file):
        print(f"Error: Input file '{data_file}' does not exist.")
        sys.exit(1)

    if not os.path.isfile(columns_file):
        print(f"Error: Columns file '{columns_file}' does not exist.")
        sys.exit(1)

    # Read column mappings with defaulting
    with open(columns_file, newline='') as f:
        reader = csv.reader(f)
        column_mappings = []
        for row in reader:
            if not row or not row[0].strip():
                continue  # skip empty or invalid rows
            input_col = row[0].strip()
            output_col = row[1].strip() if len(row) > 1 and row[1].strip() else input_col
            column_mappings.append((input_col, output_col))

    if not column_mappings:
        print("Error: No valid column mappings found in the columns file.")
        sys.exit(1)

    input_cols_to_keep = [orig for orig, _ in column_mappings]
    output_col_names = [new for _, new in column_mappings]

    with open(data_file, newline='') as f:
        reader = csv.DictReader(f)
        input_columns = reader.fieldnames

        if not input_columns:
            print("Error: Input CSV file has no header.")
            sys.exit(1)

        missing_columns = [col for col in input_cols_to_keep if col not in input_columns]
        if missing_columns:
            print(f"Error: The following columns were not found in the input file: {', '.join(missing_columns)}")
            sys.exit(1)

        filtered_rows = []
        for row in reader:
            new_row = {out_col: row[in_col] for in_col, out_col in column_mappings}
            filtered_rows.append(new_row)

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=output_col_names)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"Filtered and renamed data written to '{output_file}' successfully.")

def main():
    parser = argparse.ArgumentParser(description='Filter and optionally rename CSV columns.')
    parser.add_argument('-c', '--columns', required=True, help='CSV file with column mappings (input_col,output_col)')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file with full data')
    parser.add_argument('-o', '--output', help='Output CSV file for filtered data')

    args = parser.parse_args()

    # Determine output file name if not provided
    if args.output:
        output_file = args.output
    else:
        base, ext = os.path.splitext(args.input)
        output_file = f"{base}_filtered.csv"
    
    filter_and_rename_columns(args.input, args.columns, output_file)

if __name__ == '__main__':
    main()

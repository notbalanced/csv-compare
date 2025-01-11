# CSV Compare

This project is designed to compare entries between a reference CSV file exported from a bank and another CSV file. It identifies and displays entries that do not match, helping users to easily spot discrepancies in their financial records.

Each entry should include:
- Date in MM/DD/YYYY format
- Description
- Amount


## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd csv-compare
   ```

## Usage
```
usage: csv-compare.py [-h] [-s] [-d DATE_DELTA] [-o OUTPUT_FILE] reference_file other_file

Compare two CSV files and find mismatched entries.

positional arguments:
  reference_file        Path to the reference CSV file
  other_file            Path to the other CSV file

options:
  -h, --help            show this help message and exit
  -s, --show-matches    Show matched entries
  -d DATE_DELTA, --date-delta DATE_DELTA
                        Number of days to consider for date matching
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Path to the output CSV file
```
## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.
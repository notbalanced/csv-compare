# CSV Comparison Project

This project is designed to compare entries between a reference CSV file exported from a bank and another CSV file. It identifies and displays entries that do not match, helping users to easily spot discrepancies in their financial records.

## Project Structure

```
csv-comparison-project
├── src
│   ├── compare.py          # Main logic for comparing CSV entries
│   └── utils
│       └── file_operations.py  # Utility functions for file operations
├── data
│   ├── bank_reference.csv   # Reference data from the bank
│   ├── other_file.csv       # Other CSV data for comparison
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd csv-comparison-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure that the `data/bank_reference.csv` and `data/other_file.csv` files are populated with the appropriate data.
2. Run the comparison script:
   ```
   python src/compare.py
   ```

3. Review the output for any mismatched entries.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.
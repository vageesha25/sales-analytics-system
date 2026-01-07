from utils.file_handler import read_sales_file
from utils.data_processor import clean_sales_data

FILE_PATH = "data/sales_data.txt"

def main():
    header, records = read_sales_file(FILE_PATH)
    total, invalid, valid, cleaned = clean_sales_data(header, records)

    print(f"Total records parsed: {total}")
    print(f"Invalid records removed: {invalid}")
    print(f"Valid records after cleaning: {valid}")

if __name__ == "__main__":
    main()

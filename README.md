# 📊 Sales Analytics System  
**Module 3 – Python Programming Assignment**

---

## 📌 Project Overview

This project implements a **Sales Analytics System** that processes raw sales transaction data, cleans and validates it, integrates external product data using an API, performs multi-level analytics, generates enriched datasets, and produces a comprehensive business-ready text report.

The solution is designed as a **modular, end-to-end data pipeline**, closely reflecting real-world analytics system architecture.

---

## 🗂️ Project Structure

sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   └── api_handler.py
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
└── output/
    └── sales_report.txt


---

## 🔹 Q1 – Data File Handling

### File: `utils/file_handler.py`

#### Function: `read_sales_data(filename)`

**Responsibilities**
- Reads raw sales data from file
- Handles encoding issues (`utf-8`, `latin-1`, `cp1252`)
- Skips empty lines safely

**Returns**
- List of raw transaction strings

**Concepts Used**
- File I/O
- Encoding handling
- Defensive programming

---

## 🔹 Q2 – Data Parsing, Cleaning & Validation

### File: `utils/data_processor.py`

---

### Task 1.2 – Parse & Clean Transactions  
#### Function: `parse_transactions(raw_lines)`

**Responsibilities**
- Skip header row
- Split pipe-delimited records
- Remove commas from numeric and text fields
- Convert Quantity to `int`
- Convert UnitPrice to `float`
- Skip malformed records

**Returns**
- List of structured transaction dictionaries

---

### Task 1.3 – Validation & Filtering  
#### Function: `validate_and_filter(transactions, region=None, min_amount=None, max_amount=None)`

**Validation Rules**
- Quantity > 0
- UnitPrice > 0
- TransactionID starts with `T`
- ProductID starts with `P`
- CustomerID starts with `C`

**Optional Filters**
- Region
- Minimum transaction amount
- Maximum transaction amount

**Returns**
- Valid transactions
- Invalid record count
- Validation summary dictionary

---

## 🔹 Q3 – Data Processing & Analytics  
*(Lists, Dictionaries & Functions)*

All analytics operate **only on validated transactions**.

### File: `utils/data_processor.py`

---

### Task 2.1 – Sales Summary Analytics
- `calculate_total_revenue()` – Computes total revenue
- `region_wise_sales()` – Region-wise sales, transaction count, percentage contribution
- `top_selling_products()` – Top N products by quantity sold
- `customer_analysis()` – Customer spending, purchase count, average order value

---

### Task 2.2 – Date-Based Analysis
- `daily_sales_trend()` – Daily revenue, transaction count, unique customers
- `find_peak_sales_day()` – Identifies highest revenue day

---

### Task 2.3 – Product Performance
- `low_performing_products()` – Products with low total quantity sold

---

## 🔹 Q4 – API Integration (DummyJSON)

### File: `utils/api_handler.py`

**API Used**
- Base URL: `https://dummyjson.com/products`

---

### Task 3.1 – Fetch Product Data
- `fetch_all_products()` – Fetches products with error handling
- `create_product_mapping()` – Maps Product ID to product details

---

### Task 3.2 – Enrich Sales Data
- `enrich_sales_data()` – Adds API category, brand, rating to transactions
- Handles missing API products gracefully
- Adds `API_Match` flag

---

### Helper Function
- `save_enriched_data()` – Saves enriched data to file using pipe delimiter

---

## 🔹 Q5 – Report Generation

### File: `utils/data_processor.py`

#### Function: `generate_sales_report(transactions, enriched_transactions)`

**Generates a formatted text report containing:**

1. Header (title, timestamp, records processed)
2. Overall summary (revenue, transactions, AOV, date range)
3. Region-wise performance table
4. Top 5 products
5. Top 5 customers
6. Daily sales trend
7. Product performance analysis
8. API enrichment summary

**Output File**
- `output/sales_report.txt`

---

## 🔹 Q6 – Main Application (CLI Orchestration)

### File: `main.py`

#### Function: `main()`

**Execution Flow**
1. Display welcome banner
2. Read sales data
3. Parse and clean records
4. Display filter options
5. Accept user filter input (optional)
6. Validate transactions
7. Perform analytics
8. Fetch API product data
9. Enrich sales data
10. Save enriched dataset
11. Generate final report
12. Display success messages

**Error Handling**
- Entire workflow wrapped in `try-except`
- User-friendly error messages
- Application does not crash on failures

---

## ▶️ How to Run the Application

### Prerequisites
- Python 3.x
- `requests` library

```bash
pip install requests

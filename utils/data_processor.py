# =========================================================
# Q1 / Q2 / Q3 – DATA PROCESSING & ANALYTICS
# File: utils/data_processor.py
# =========================================================


# ---------------------------------------------------------
# Q2 – TASK 1.2: PARSE & CLEAN DATA
# ---------------------------------------------------------
def parse_transactions(raw_lines):
    """
    Parses raw sales data lines into a list of dictionaries.
    """
    transactions = []
    header_skipped = False

    for line in raw_lines:
        if not header_skipped:
            header_skipped = True
            continue

        parts = line.split("|")

        if len(parts) != 8:
            continue

        try:
            txn_id, date, prod_id, prod_name, qty, price, cust_id, region = parts

            transactions.append({
                "TransactionID": txn_id.strip(),
                "Date": date.strip(),
                "ProductID": prod_id.strip(),
                "ProductName": prod_name.replace(",", "").strip(),
                "Quantity": int(qty.replace(",", "")),
                "UnitPrice": float(price.replace(",", "")),
                "CustomerID": cust_id.strip(),
                "Region": region.strip()
            })

        except Exception:
            continue

    return transactions


# ---------------------------------------------------------
# Q2 – TASK 1.3: VALIDATION & FILTERING
# ---------------------------------------------------------
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid = 0

    for tx in transactions:
        try:
            if (
                tx["Quantity"] <= 0
                or tx["UnitPrice"] <= 0
                or not tx["TransactionID"].startswith("T")
                or not tx["ProductID"].startswith("P")
                or not tx["CustomerID"].startswith("C")
            ):
                invalid += 1
                continue

            amount = tx["Quantity"] * tx["UnitPrice"]

            if region and tx["Region"] != region:
                continue
            if min_amount and amount < min_amount:
                continue
            if max_amount and amount > max_amount:
                continue

            valid.append(tx)

        except Exception:
            invalid += 1

    summary = {
        "total_input": len(transactions),
        "invalid": invalid,
        "final_count": len(valid)
    }

    return valid, invalid, summary


# =========================================================
# Q3 – TASK 2.1: SALES SUMMARY
# =========================================================
def calculate_total_revenue(transactions):
    total = 0.0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return total


def region_wise_sales(transactions):
    region_data = {}
    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0,
                "transactions": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transactions"] += 1

    for r in region_data:
        region_data[r]["percentage"] = round(
            (region_data[r]["total_sales"] / total_revenue) * 100, 2
        )

    return dict(
        sorted(region_data.items(), key=lambda x: x[1]["total_sales"], reverse=True)
    )


def top_selling_products(transactions, n=5):
    products = {}

    for tx in transactions:
        p = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if p not in products:
            products[p] = {"qty": 0, "revenue": 0}

        products[p]["qty"] += qty
        products[p]["revenue"] += revenue

    result = [(p, v["qty"], v["revenue"]) for p, v in products.items()]
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        c = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if c not in customers:
            customers[c] = {
                "total_spent": 0,
                "count": 0,
                "products": set()
            }

        customers[c]["total_spent"] += amount
        customers[c]["count"] += 1
        customers[c]["products"].add(tx["ProductName"])

    final = {}
    for c, v in customers.items():
        final[c] = {
            "total_spent": v["total_spent"],
            "purchase_count": v["count"],
            "avg_order_value": round(v["total_spent"] / v["count"], 2),
            "products_bought": list(v["products"])
        }

    return dict(sorted(final.items(), key=lambda x: x[1]["total_spent"], reverse=True))


# =========================================================
# Q3 – TASK 2.2: DATE-BASED ANALYSIS
# =========================================================
def daily_sales_trend(transactions):
    daily = {}

    for tx in transactions:
        d = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if d not in daily:
            daily[d] = {
                "revenue": 0,
                "transactions": 0,
                "customers": set()
            }

        daily[d]["revenue"] += revenue
        daily[d]["transactions"] += 1
        daily[d]["customers"].add(tx["CustomerID"])

    result = {}
    for d in sorted(daily):
        result[d] = {
            "revenue": daily[d]["revenue"],
            "transaction_count": daily[d]["transactions"],
            "unique_customers": len(daily[d]["customers"])
        }

    return result


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    peak = max(daily, key=lambda d: daily[d]["revenue"])

    return (
        peak,
        daily[peak]["revenue"],
        daily[peak]["transaction_count"]
    )


# =========================================================
# Q3 – TASK 2.3: PRODUCT PERFORMANCE
# =========================================================
def low_performing_products(transactions, threshold=10):
    products = {}

    for tx in transactions:
        p = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if p not in products:
            products[p] = {"qty": 0, "revenue": 0}

        products[p]["qty"] += qty
        products[p]["revenue"] += revenue

    result = [
        (p, v["qty"], v["revenue"])
        for p, v in products.items()
        if v["qty"] < threshold
    ]

    result.sort(key=lambda x: x[1])
    return result


# =========================================================
# Q5 – Generate Report
# =========================================================

from datetime import datetime
from collections import defaultdict


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted sales report
    """

    # ----------------------------
    # BASIC METRICS
    # ----------------------------
    total_transactions = len(transactions)
    total_revenue = sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [tx["Date"] for tx in transactions]
    start_date, end_date = min(dates), max(dates)

    # ----------------------------
    # REGION-WISE PERFORMANCE
    # ----------------------------
    region_data = defaultdict(lambda: {"revenue": 0, "count": 0})

    for tx in transactions:
        region = tx["Region"]
        region_data[region]["revenue"] += tx["Quantity"] * tx["UnitPrice"]
        region_data[region]["count"] += 1

    region_rows = []
    for region, data in region_data.items():
        percent = (data["revenue"] / total_revenue) * 100
        region_rows.append((region, data["revenue"], percent, data["count"]))

    region_rows.sort(key=lambda x: x[1], reverse=True)

    # ----------------------------
    # TOP 5 PRODUCTS
    # ----------------------------
    product_data = defaultdict(lambda: {"qty": 0, "revenue": 0})

    for tx in transactions:
        product = tx["ProductName"]
        product_data[product]["qty"] += tx["Quantity"]
        product_data[product]["revenue"] += tx["Quantity"] * tx["UnitPrice"]

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    # ----------------------------
    # TOP 5 CUSTOMERS
    # ----------------------------
    customer_data = defaultdict(lambda: {"spent": 0, "count": 0})

    for tx in transactions:
        cid = tx["CustomerID"]
        customer_data[cid]["spent"] += tx["Quantity"] * tx["UnitPrice"]
        customer_data[cid]["count"] += 1

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ----------------------------
    # DAILY SALES TREND
    # ----------------------------
    daily_data = defaultdict(lambda: {"revenue": 0, "count": 0, "customers": set()})

    for tx in transactions:
        date = tx["Date"]
        daily_data[date]["revenue"] += tx["Quantity"] * tx["UnitPrice"]
        daily_data[date]["count"] += 1
        daily_data[date]["customers"].add(tx["CustomerID"])

    daily_rows = sorted(daily_data.items())

    # ----------------------------
    # PRODUCT PERFORMANCE ANALYSIS
    # ----------------------------
    best_day = max(daily_rows, key=lambda x: x[1]["revenue"])

    low_products = [
        (p, v["qty"])
        for p, v in product_data.items()
        if v["qty"] < 10
    ]

    avg_region_value = {
        r: region_data[r]["revenue"] / region_data[r]["count"]
        for r in region_data
    }

    # ----------------------------
    # API ENRICHMENT SUMMARY
    # ----------------------------
    enriched_count = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
    enrichment_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    failed_products = {
        tx["ProductName"]
        for tx in enriched_transactions
        if not tx.get("API_Match")
    }

    # ----------------------------
    # WRITE REPORT
    # ----------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 44 + "\n")
        f.write("       SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"     Records Processed: {total_transactions}\n")
        f.write("=" * 44 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {start_date} to {end_date}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Region':<10}{'Sales':>12}{'% Total':>10}{'Txns':>8}\n")
        for r, rev, pct, cnt in region_rows:
            f.write(f"{r:<10}₹{rev:>10,.0f}{pct:>9.2f}%{cnt:>8}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Product':<20}{'Qty':>6}{'Revenue':>12}\n")
        for i, (p, v) in enumerate(top_products, 1):
            f.write(f"{i:<6}{p:<20}{v['qty']:>6}₹{v['revenue']:>10,.0f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<10}{'Spent':>14}{'Orders':>10}\n")
        for i, (c, v) in enumerate(top_customers, 1):
            f.write(f"{i:<6}{c:<10}₹{v['spent']:>12,.0f}{v['count']:>10}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>12}{'Txns':>8}{'Customers':>12}\n")
        for d, v in daily_rows:
            f.write(f"{d:<12}₹{v['revenue']:>10,.0f}{v['count']:>8}{len(v['customers']):>12}\n")
        f.write("\n")

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best Selling Day: {best_day[0]} (₹{best_day[1]['revenue']:,.0f})\n")
        f.write("Low Performing Products (<10 units):\n")
        for p, q in low_products:
            f.write(f" - {p} ({q})\n")
        f.write("\nAverage Transaction Value per Region:\n")
        for r, v in avg_region_value.items():
            f.write(f" - {r}: ₹{v:,.2f}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {enrichment_rate:.2f}%\n")
        if failed_products:
            f.write("Products not enriched:\n")
            for p in failed_products:
                f.write(f" - {p}\n")
        else:
            f.write("All products enriched successfully\n")

    print(f"Sales report generated at {output_file}")

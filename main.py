from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def main():
    """
    Main execution function
    """
    try:
        print("=" * 40)
        print("      SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # -------------------------------------------------
        # 1. Read sales data
        # -------------------------------------------------
        print("\n[1/10] Reading sales data...")
        raw = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw)} transactions")

        # -------------------------------------------------
        # 2. Parse and clean data
        # -------------------------------------------------
        print("\n[2/10] Parsing and cleaning data...")
        parsed = parse_transactions(raw)
        print(f"✓ Parsed {len(parsed)} records")

        # -------------------------------------------------
        # 3. Show filter options
        # -------------------------------------------------
        regions = sorted({tx["Region"] for tx in parsed if tx["Region"]})
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in parsed]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if apply_filter == "y":
            region_filter = input("Enter region (or leave blank): ").strip() or None

            min_val = input("Enter minimum amount (or leave blank): ").strip()
            max_val = input("Enter maximum amount (or leave blank): ").strip()

            min_amount = float(min_val) if min_val else None
            max_amount = float(max_val) if max_val else None

        # -------------------------------------------------
        # 4. Validate transactions
        # -------------------------------------------------
        print("\n[4/10] Validating transactions...")
        valid, invalid, summary = validate_and_filter(
            parsed,
            region=region_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )
        print(f"✓ Valid: {len(valid)} | Invalid: {invalid}")

        # -------------------------------------------------
        # 5. Perform data analysis
        # -------------------------------------------------
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid)
        region_wise_sales(valid)
        top_selling_products(valid)
        customer_analysis(valid)
        daily_sales_trend(valid)
        find_peak_sales_day(valid)
        low_performing_products(valid)
        print("✓ Analysis complete")

        # -------------------------------------------------
        # 6. Fetch API data
        # -------------------------------------------------
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products")

        # -------------------------------------------------
        # 7. Enrich sales data
        # -------------------------------------------------
        print("\n[7/10] Enriching sales data...")
        enriched = enrich_sales_data(valid, product_mapping)
        enriched_count = sum(1 for tx in enriched if tx.get("API_Match"))
        rate = (enriched_count / len(enriched)) * 100 if enriched else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched)} transactions ({rate:.1f}%)")

        # -------------------------------------------------
        # 8. Save enriched data
        # -------------------------------------------------
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # -------------------------------------------------
        # 9. Generate report
        # -------------------------------------------------
        print("\n[9/10] Generating report...")
        generate_sales_report(valid, enriched)
        print("✓ Report saved to: output/sales_report.txt")

        # -------------------------------------------------
        # 10. Done
        # -------------------------------------------------
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred:")
        print(str(e))
        print("Please check inputs or try again.")


if __name__ == "__main__":
    main()

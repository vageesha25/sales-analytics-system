def clean_sales_data(header, records):
    total = 0
    invalid = 0
    valid = 0
    cleaned_records = []

    for row in records:
        total += 1

        try:
            data = dict(zip(header, row))

            txn_id = data["TransactionID"].strip()
            product = data["ProductName"].replace(",", "")
            quantity = int(data["Quantity"].replace(",", ""))
            price = float(data["UnitPrice"].replace(",", ""))
            customer = data["CustomerID"].strip()
            region = data["Region"].strip()

            # INVALID CONDITIONS
            if (
                not txn_id.startswith("T")
                or not customer
                or not region
                or quantity <= 0
                or price <= 0
            ):
                invalid += 1
                continue

            cleaned_records.append({
                "TransactionID": txn_id,
                "ProductName": product,
                "Quantity": quantity,
                "UnitPrice": price,
                "CustomerID": customer,
                "Region": region
            })
            valid += 1

        except Exception:
            invalid += 1

    return total, invalid, valid, cleaned_records

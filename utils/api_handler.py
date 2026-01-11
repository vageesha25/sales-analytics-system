import requests

BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)

        if response.status_code == 200:
            data = response.json()
            print("API fetch successful")
            return data.get("products", [])
        else:
            print("API fetch failed with status:", response.status_code)
            return []

    except requests.RequestException as e:
        print("API connection error:", e)
        return []

def create_product_mapping(api_products):
    """
    Creates mapping of product ID to product info
    """
    mapping = {}

    for product in api_products:
        try:
            product_id = product["id"]
            mapping[product_id] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating")
            }
        except KeyError:
            continue

    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches sales transactions with API product information
    """
    enriched = []

    for tx in transactions:
        tx_copy = tx.copy()

        try:
            product_id_str = tx["ProductID"].replace("P", "")
            product_id = int(product_id_str)
        except Exception:
            product_id = None

        api_product = product_mapping.get(product_id)

        if api_product:
            tx_copy["API_Category"] = api_product.get("category")
            tx_copy["API_Brand"] = api_product.get("brand")
            tx_copy["API_Rating"] = api_product.get("rating")
            tx_copy["API_Match"] = True
        else:
            tx_copy["API_Category"] = None
            tx_copy["API_Brand"] = None
            tx_copy["API_Rating"] = None
            tx_copy["API_Match"] = False

        enriched.append(tx_copy)

    return enriched

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to file
    """
    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(header) + "\n")

        for tx in enriched_transactions:
            row = [
                str(tx.get(col, "")) if tx.get(col) is not None else ""
                for col in header
            ]
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")

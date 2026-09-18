"""Olist ETL pipeline. Run from repository root with:
python notebooks/01_data_pipeline.py
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
]

missing = [name for name in REQUIRED_FILES if not (RAW_DIR / name).exists()]
if missing:
    raise FileNotFoundError(
        "Missing raw dataset files: "
        + ", ".join(missing)
        + f"\nPlace the downloaded CSV files in: {RAW_DIR}"
    )

orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")

df = orders.merge(items, on="order_id", how="left")
df = df.merge(customers, on="customer_id", how="left")
df = df.merge(products, on="product_id", how="left")

df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"], errors="coerce"
)
df["product_category_name"] = df["product_category_name"].fillna("Unknown")
df["total_item_value"] = df["price"].fillna(0) + df["freight_value"].fillna(0)

output_path = PROCESSED_DIR / "master_sales_data.csv"
df.to_csv(output_path, index=False)

print(f"Success! Saved {len(df):,} rows to {output_path}")
print(f"Columns: {len(df.columns)}")

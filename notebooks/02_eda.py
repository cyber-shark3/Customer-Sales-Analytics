"""Exploratory data analysis for the cleaned Olist master table.

Run from the repository root:
    python notebooks/02_eda.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "master_sales_data.csv"
OUTPUT_DIR = ROOT / "dashboard" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Processed dataset not found: {DATA_PATH}. "
        "Run notebooks/01_data_pipeline.py first."
    )

df = pd.read_csv(DATA_PATH)
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"], errors="coerce"
)

# -------------------------
# 1. Data quality checks
# -------------------------
print("\n=== DATA OVERVIEW ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")
print(f"Unique orders: {df['order_id'].nunique():,}")
print(f"Unique customers: {df['customer_id'].nunique():,}")
print(f"Unique products: {df['product_id'].nunique():,}")

print("\n=== MISSING VALUES (TOP 15) ===")
print(df.isna().sum().sort_values(ascending=False).head(15))

# -------------------------
# 2. Core business KPIs
# -------------------------
total_revenue = df["price"].fillna(0).sum()
total_freight = df["freight_value"].fillna(0).sum()
total_value = df["total_item_value"].fillna(0).sum()
average_item_value = df["total_item_value"].fillna(0).mean()
average_delivery_days = pd.NA

if "order_delivered_customer_date" in df.columns:
    delivered = pd.to_datetime(
        df["order_delivered_customer_date"], errors="coerce"
    )
    purchase = df["order_purchase_timestamp"]
    delivery_days = (delivered - purchase).dt.total_seconds() / 86400
    delivery_days = delivery_days[delivery_days >= 0]
    if not delivery_days.empty:
        average_delivery_days = delivery_days.mean()

print("\n=== CORE KPIs ===")
print(f"Product revenue: {total_revenue:,.2f}")
print(f"Freight value: {total_freight:,.2f}")
print(f"Total item value: {total_value:,.2f}")
print(f"Average item value: {average_item_value:,.2f}")
print(
    "Average delivery days: "
    + (
        f"{average_delivery_days:.2f}"
        if pd.notna(average_delivery_days)
        else "N/A"
    )
)

# -------------------------
# 3. Revenue by month
# -------------------------
monthly = (
    df.dropna(subset=["order_purchase_timestamp"])
    .set_index("order_purchase_timestamp")["price"]
    .fillna(0)
    .resample("MS")
    .sum()
)

plt.figure(figsize=(12, 5))
monthly.plot()
plt.title("Monthly Product Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=150)
plt.close()

# -------------------------
# 4. Revenue by customer state
# -------------------------
if "customer_state" in df.columns:
    state_revenue = (
        df.groupby("customer_state")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 5))
    state_revenue.sort_values().plot(kind="barh")
    plt.title("Top 10 States by Product Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("State")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_states_revenue.png", dpi=150)
    plt.close()

# -------------------------
# 5. Revenue by product category
# -------------------------
if "product_category_name" in df.columns:
    category_revenue = (
        df.groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))
    category_revenue.sort_values().plot(kind="barh")
    plt.title("Top 10 Product Categories by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_categories_revenue.png", dpi=150)
    plt.close()

print("\n=== EDA COMPLETE ===")
print(f"Charts saved to: {OUTPUT_DIR}")

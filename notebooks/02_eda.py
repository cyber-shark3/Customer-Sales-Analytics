"""Exploratory analysis for the cleaned Olist master table."""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "master_sales_data.csv"
OUTPUT_DIR = ROOT / "dashboard" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["order_purchase_timestamp"])

print("\nDataset shape:", df.shape)
print("\nMissing values:")
print(df.isna().sum().sort_values(ascending=False).head(15))

print("\nTop product categories by revenue:")
print(
    df.groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

monthly = (
    df.set_index("order_purchase_timestamp")["price"]
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

print("\nEDA complete. Chart saved to dashboard/screenshots/monthly_revenue.png")

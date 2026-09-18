# Raw Olist Dataset

The Olist CSV files are tracked with Git LFS because the dataset is too large for normal Git storage.

Dataset files:
- olist_customers_dataset.csv
- olist_geolocation_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv
- olist_order_reviews_dataset.csv
- olist_orders_dataset.csv
- olist_products_dataset.csv
- olist_sellers_dataset.csv
- product_category_name_translation.csv

## Add the local dataset

From the repository root:

```bash
git lfs install
git lfs pull
git add data/raw/
git commit -m "Add Olist raw dataset"
git push origin main
```

The local dataset archive supplied for this project contains all nine CSV files.

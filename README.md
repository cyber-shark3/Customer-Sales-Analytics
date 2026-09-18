# 📊 E-Commerce Customer & Sales Analytics

## Executive Summary
A comprehensive analysis of the Olist Brazilian E-Commerce dataset to identify revenue drivers, customer behaviour, product performance, delivery bottlenecks, review patterns, and regional trends.

## Business Problem
The business needs to understand where revenue comes from, which customers and products matter most, where delivery performance breaks down, and how freight costs and regional patterns affect the customer experience.

## Tech Stack
- **Python:** Pandas, NumPy
- **SQL:** SQLite / PostgreSQL
- **Visualisation:** Matplotlib, Seaborn
- **Dashboard:** Power BI
- **Workflow:** Jupyter / Python scripts

## Project Structure
```
Customer-Sales-Analytics/
├── data/
│   ├── raw/
│   └── processed/
├── sql/
│   ├── 01_create_schema.sql
│   └── 02_kpi_queries.sql
├── notebooks/
│   ├── 01_data_pipeline.py
│   └── 02_eda.py
├── dashboard/
│   └── screenshots/
└── insights/
    └── strategic_recommendations.md
```

## Dataset
The project uses the Olist Brazilian E-Commerce Public Dataset. Raw CSV files are intentionally ignored by Git because of their size.

Put the downloaded files in `data/raw/`.

Expected core files:
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_products_dataset.csv`

## ETL Pipeline
1. Loads the raw Olist tables.
2. Joins orders, order items, customers and products.
3. Cleans timestamps and missing product categories.
4. Calculates item value including freight.
5. Saves a reusable master analytical table to `data/processed/master_sales_data.csv`.

Run from the repository root:

```bash
python notebooks/01_data_pipeline.py
```

## Planned Analysis
- Revenue and sales trends
- Customer behaviour and repeat purchasing
- Product/category performance
- Delivery times and delays
- Freight cost patterns
- Review-score relationships
- Regional sales and delivery patterns

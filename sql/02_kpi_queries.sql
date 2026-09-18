-- Core KPI queries for the Olist analysis.

SELECT
    ROUND(SUM(price), 2) AS product_revenue,
    ROUND(SUM(freight_value), 2) AS freight_value,
    ROUND(SUM(price + freight_value), 2) AS gross_item_value
FROM order_items;

SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY revenue DESC;

SELECT
    COALESCE(p.product_category_name, 'Unknown') AS category,
    COUNT(DISTINCT oi.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS revenue,
    ROUND(AVG(oi.price), 2) AS average_item_price
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
GROUP BY category
ORDER BY revenue DESC
LIMIT 20;

SELECT
    ROUND(AVG(
        julianday(o.order_delivered_customer_date)
        - julianday(o.order_purchase_timestamp)
    ), 2) AS avg_delivery_days
FROM orders o
WHERE o.order_delivered_customer_date IS NOT NULL;

SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.price), 2) AS customer_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_unique_id
ORDER BY order_count DESC, customer_revenue DESC;

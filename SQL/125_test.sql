SELECT *
FROM products;

SELECT supplier_id, product_name, unit_price, units_in_stock, SUM(unit_price) OVER w, SUM(units_in_stock) OVER w
FROM products
WINDOW w AS (PARTITION BY supplier_id ORDER BY unit_price DESC); --, unit_in_stock
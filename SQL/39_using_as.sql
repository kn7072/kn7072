SELECT contact_name, company_name, phone, first_name, last_name, title,
       order_date, product_name, ship_country, products.unit_price, quantity, discount
FROM orders
JOIN order_details USING(order_id) --ON orders.order_id = order_details.order_id
JOIN products USING(product_id) --ON order_details.product_id = products.product_id
JOIN customers USING(customer_id) --ON orders.customer_id = customers.customer_id
JOIN employees USING(employee_id) --ON orders.employee_id = employees.employee_id
WHERE ship_country = 'USA';

SELECT COUNT(*) AS employees_count
FROM employees;

SELECT COUNT(DISTINCT country) AS country
FROM employees;

SELECT category_id, SUM(units_in_stock) AS units_in_stock
FROM products
GROUP BY category_id
ORDER BY units_in_stock DESC
LIMIT 5;

SELECT category_id, SUM(unit_price * units_in_stock) AS total_price
FROM products
WHERE discontinued != 1
GROUP BY category_id
HAVING SUM(unit_price * units_in_stock) > 5000 -- EROR total_price > 5000 (нельзя использовать алиасы в WHERE и HAVING)
ORDER BY total_price DESC;
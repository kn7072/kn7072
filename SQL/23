SELECT DISTINCT country
FROM customers
ORDER BY country DESC; -- ASC

SELECT DISTINCT country, city
FROM customers
ORDER BY country DESC, city ASC;
--
SELECT ship_city, order_date
FROM orders
WHERE ship_city = 'London'
ORDER BY order_date;

SELECT MIN(order_date) -- MAX, AVG
FROM orders
WHERE ship_city = 'London';

SELECT AVG(unit_price)
FROM products
WHERE discontinued != 1;

SELECT SUM(units_in_stock)
FROM products
WHERE discontinued != 1;
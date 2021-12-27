-- 1
SELECT *
FROM orders
WHERE ship_country IN ('France', 'Austria', 'Spain');

--2
SELECT *
FROM orders
ORDER BY required_date DESC, shipped_date ASC; 

--3
SELECT MIN(units_price)
FROM products
WHERE units_in_stock > 30;

--4
SELECT MAX(units_in_stock)
FROM products
WHERE units_price > 30;

--5
SELECT AVG(shipped_date - order_date)
FROM orders
WHERE ship_country = 'USA';

--6
SELECT SUM(unit_price * units_in_stock)
FROM products
WHERE discontinued != 1;


--1
SELECT *
FROM orders
WHERE ship_country LIKE 'U%';

--2
SELECT order_id, customer_id, freight, ship_country
FROM orders
WHERE ship_country LIKE 'N%'
ORDER BY freight DESC
LIMIT 5;

--3
SELECT first_name, last_name, home_phone, region
FROM employees
WHERE region IS NULL;

--4
SELECT COUNT(*)
FROM customers
WHERE region IS NOT NULL;

--5
SELECT country, COUNT(*)
FROM suppliers
GROUP BY country
ORDER BY COUNT(*) DESC;

--6
SELECT ship_country, SUM(freight)
FROM orders
WHERE ship_region IS NOT NULL
GROUP BY ship_country
HAVING SUM(freight) > 2750
ORDER BY SUM(freight) DESC;

--7
SELECT country
FROM customers
UNION
SELECT country
FROM suppliers
ORDER BY country ASC;

--8
SELECT country
FROM customers
INTERSECT
SELECT country
FROM suppliers
INTERSECT 
SELECT country
FROM employees;

--9
SELECT country
FROM customers
INTERSECT
SELECT country
FROM suppliers
EXCEPT
SELECT country
FROM employees;

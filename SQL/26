SELECT last_name, first_name
FROM employees
WHERE first_name LIKE '%n' OR last_name LIKE 'Bu%';

SELECT first_name
FROM employees
WHERE last_name LIKE '_ucha%'
LIMIT 10;

--IS NULL  IS NOT NULL
SELECT ship_city, ship_region, ship_country
FROM orders
WHERE ship_region IS NULL; -- IS NOT NULL

--GROUP BY
SELECT ship_country, COUNT(*)
FROM orders 
WHERE freight > 50
GROUP BY ship_country
ORDER BY COUNT(*) DESC;

SELECT category_id, SUM(units_in_stock)
FROM products
GROUP BY category_id
ORDER BY SUM(units_in_stock) DESC
LIMIT 5;

--HAVING постфильтрация
 SELECT category_id, SUM(unit_price * units_in_stock)
 FROM products
 WHERE discontinued != 1
 GROUP BY category_id
 HAVING SUM(unit_price * units_in_stock) > 5000 -- ПЕРЕД ORDER BY
 ORDER BY SUM(unit_price * units_in_stock) DESC;
 
 --операции на множествах
 SELECT country
 FROM customers
 UNION --ОБЪЕДИНЕНИЕ запросов, UNION страняет дубликаты, UNION ALL -дубликаты не устраняются
 SELECT country
 FROM employees;
 
 SELECT country
 FROM customers
 INTERSECT -- ПЕРЕСЕЧЕНИЕ
 SELECT country
 FROM suppliers;
 
 SELECT country
 FROM customers
 EXCEPT --ИКЛЮЧЕНИЕ 
 SELECT country
 FROM suppliers;

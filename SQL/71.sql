SELECT *
FROM orders
LIMIT 10;

-- COALESCE возвращает 'unknow' если ship_region = NULL
SELECT order_id, order_date, COALESCE(ship_region, 'unknow') AS ship_region
FROM orders
LIMIT 10;

SELECT last_name, first_name, COALESCE(region, 'N/A') AS region
FROM employees;

-- NULLIF возвращает NULL если аргументы равны, если значения не равны - возвращает первое значение
-- в примере ниже, если city - пустая строка, NULLIF вернет NULL, а COALESCE вернет 'unknow'
SELECT contact_name, COALESCE(NULLIF(city, ''), 'unknow') AS city
FROM customers;

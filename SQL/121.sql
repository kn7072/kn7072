SELECT company_name
FROM suppliers
WHERE country IN (SELECT country FROM customers);

--CTE временная таблица
WITH customer_countries AS
(
	SELECT country FROM customers
)

SELECT company_name
FROM suppliers
WHERE country IN (SELECT * FROM customer_countries);

SELECT company_name
FROM suppliers
WHERE NOT EXISTS 
	(
		SELECT product_id
		FROM products
		JOIN order_details USING(product_id)
		JOIN orders USING(order_id)
		WHERE suppliers.supplier_id = products.supplier_id AND
			order_date BETWEEN '1998-02-01' AND '1998-02-04'
	);
	
SELECT company_name
FROM products
JOIN order_details USING(product_id)
JOIN orders USING(order_id)
JOIN suppliers USING(supplier_id)
WHERE order_date BETWEEN '1998-02-01' AND '1998-02-04';
	
WITH filtered AS
(
	SELECT company_name, suppliers.supplier_id
	FROM products
	JOIN order_details USING(product_id)
	JOIN orders USING(order_id)
	JOIN suppliers USING(supplier_id)
	WHERE order_date BETWEEN '1998-02-01' AND '1998-02-04'
)
SELECT company_name
FROM suppliers
WHERE supplier_id NOT IN (SELECT supplier_id FROM filtered);

--122
DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
	employee_id INT PRIMARY KEY,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	manager_id INT,
	FOREIGN KEY (manager_id) REFERENCES employee (employee_id) ON DELETE CASCADE
	--ON DELETE CASCADE при удалении записей в employee
);

INSERT INTO employee (
	employee_id,
	first_name,
	last_name,
	manager_id
)
VALUES
	(1, 'windy', 'hays', NULL),
	(2, 'ava', 'christensen', 1),
	(3, 'hassan', 'conner', 1),
	(4, 'ann', 'reeves', 2),
	(5, 'sau', 'norman', 2),
	(6, 'kelsie', 'hays', 3),
	(7, 'torry', 'goff', 3),
	(8, 'salley', 'leater', 3);
	
WITH RECURSIVE submission(sub_line, employee_id) AS
(
	SELECT last_name, employee_id FROM employee
	WHERE manager_id IS NULL
	UNION ALL
	SELECT sub_line || ' -> ' || e.last_name, e.employee_id
	FROM employee e, submission s --рекурсивный вызов
	WHERE e.manager_id = s.employee_id
)
SELECT * FROM submission;


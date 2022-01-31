--1
CREATE VIEW my_view AS
SELECT order_date, required_date, shipped_date, ship_postal_code, company_name,
	contact_name, phone, last_name, first_name, title
FROM orders
JOIN customers USING(customer_id) --ON orders.customer_id = customers.customer_id
JOIN employees USING(employee_id); --ON orders.employee_id = employees.employee_id

--Сделать select к созданному представлению, выведя все записи, где order_date больше 1го января 1997 года.
SELECT * FROM my_view
WHERE order_date > '1997-01-01'
LIMIT 10;

--2
CREATE VIEW my_view_2 AS
SELECT order_date, required_date, shipped_date, ship_postal_code, 
	ship_country, company_name, contact_name, phone, last_name, first_name, title
FROM orders
JOIN customers USING(customer_id)
JOIN employees USING(employee_id);

CREATE OR REPLACE VIEW my_view_2 AS
SELECT order_date, required_date, shipped_date, ship_postal_code, 
	ship_country, company_name, contact_name, phone, last_name, first_name, title,   
	ship_country, postal_code, reports_to
FROM orders
JOIN customers USING(customer_id)
JOIN employees USING(employee_id);

DROP VIEW IF EXISTS my_view_2;

CREATE OR REPLACE VIEW my_view_2 AS
SELECT order_date, required_date, shipped_date, ship_postal_code, 
	ship_country, company_name, contact_name, phone, last_name, first_name, title,   
	c.postal_code, reports_to
FROM orders
JOIN customers c USING(customer_id)
JOIN employees USING(employee_id);

SELECT * FROM my_view_2
ORDER BY ship_country DESC;

--3
CREATE OR REPLACE VIEW products_active AS
SELECT *
FROM products
WHERE discontinued = 0
WITH LOCAL CHECK OPTION;

SELECT * FROM products_active
LIMIT 5;

SELECT MAX(product_id) FROM products;

INSERT INTO products_active
VALUES (78, 'Aniseed Syrup',	1, 2, '12 - 550 ml bottles', 10, 13, 70, 25,      1);




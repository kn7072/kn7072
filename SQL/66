CREATE VIEW products_suppliers_categories AS
SELECT product_name, quantity_per_unit, unit_price, units_in_stock,
company_name, contact_name, phone, category_name, description
FROM products
JOIN suppliers USING(supplier_id)
JOIN categories USING(category_id);

SELECT * FROM products_suppliers_categories;

SELECT * FROM products_suppliers_categories
WHERE unit_price > 20;

DROP VIEW IF EXISTS products_suppliers_categories;

-- 65
SELECT * FROM orders;

CREATE VIEW heavy_orders AS
SELECT *
FROM orders
WHERE freight > 50;

SELECT *
FROM heavy_orders
ORDER BY freight;

CREATE OR REPLACE VIEW heavy_orders AS -- изменяем view
SELECT *
FROM orders
WHERE freight > 100;

-- попробуем расшишить(добавить новые столбцв) к view - должны получить ошибку - таковы ограничения(нельзя добавлять столбцы к существующей view)
DROP VIEW IF EXISTS products_suppliers_categories;

-- создаем view
CREATE VIEW products_suppliers_categories AS
SELECT product_name, quantity_per_unit, unit_price, units_in_stock,
company_name, contact_name, phone, category_name, description
FROM products
JOIN suppliers USING(supplier_id)
JOIN categories USING(category_id);

-- ERROR:  cannot change name of view column "company_name" to "discontinued"
CREATE OR REPLACE VIEW products_suppliers_categories AS
SELECT product_name, quantity_per_unit, unit_price, units_in_stock,      discontinued,
company_name, contact_name, phone, category_name, description
FROM products
JOIN suppliers USING(supplier_id)
JOIN categories USING(category_id);

-- переименовать view
ALTER TABLE products_suppliers_categories RENAME TO products_suppliers_categories_new;


-- 66
CREATE OR REPLACE VIEW heavy_orders AS
SELECT *
FROM orders
WHERE freight > 50
WITH LOCAL CHECK OPTION; --заставляет проверять данные, добавляемые через insert(данные не добавятся если не будут соответствовать условию where)

SELECT *
FROM heavy_orders
ORDER BY freight;

SELECT MAX(order_id)
FROM orders;

INSERT INTO heavy_orders
VALUES (11079, 'RICAR',	4, '1997-08-06', '1997-09-03', '1997-08-11', 3, 1, --1(freight) меньше 50 (WHERE freight > 50) получаем ошибку
		'Ricardo Adocicados', 'Av. Copacabana, 267', 'Rio de Janeiro', 'RJ', '02389-890', 'Brazil');



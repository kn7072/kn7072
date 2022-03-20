-- https://postgrespro.ru/docs/postgrespro/14/transaction-iso

-- В рамках транзакции с уровнем изоляции Repeatable Read выполнить следующие операции:
-- - заархивировать (SELECT INTO или CREATE TABLE AS) заказчиков, которые сделали покупок менее чем на 2000 у.е.
-- - удалить из таблицы заказчиков всех заказчиков, которые были предварительно заархивированы (подсказка: для этого придётся удалить данные из связанных таблиц)
BEGIN TRANSACTION ISOLATION LEVEL Repeatable Read;

DROP TABLE IF EXISTS customers_archive;

CREATE TABLE customers_archive AS
SELECT customer_id, company_name, SUM(unit_price * quantity) AS total
	FROM orders
	JOIN order_details USING(order_id)
	JOIN customers USING(customer_id)
	GROUP BY company_name, customer_id
	HAVING SUM(unit_price * quantity) < 2000
	ORDER BY SUM(unit_price * quantity) DESC;

	
SAVEPOINT before_delete;

SELECT COUNT(*) FROM customers_archive;
--ROLLBACK;

DELETE FROM order_details
WHERE order_id IN (SELECT order_id 
				   FROM orders
				   WHERE customer_id IN (SELECT customer_id FROM customers_archive)
				  );

DELETE FROM orders
WHERE customer_id IN (SELECT customer_id FROM customers_archive);

DELETE FROM customers
WHERE customer_id IN (SELECT customer_id FROM customers_archive);
	
COMMIT;

-----------------------------------------------------------------------------------
-- В рамках транзакции выполнить следующие операции:
-- - заархивировать все продукты, снятые с продажи (см. колонку discontinued)
-- - поставить savepoint после архивации
-- - удалить из таблицы продуктов все продукты, которые были заархивированы
-- - откатиться к savepoint
-- - закоммитить тразнакцию

BEGIN;

CREATE TABLE discontinued_products AS
SELECT * FROM products
WHERE discontinued = 1;

SAVEPOINT after_archive;

DELETE FROM order_details
WHERE product_id IN (SELECT product_id FROM discontinued_products);

DELETE FROM products
WHERE discontinued = 1;

ROLLBACK TO SAVEPOINT after_archive;

SELECT COUNT(*) FROM products WHERE discontinued = 1;
--ROLLBACK;
COMMIT;

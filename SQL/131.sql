-- коды ошибок https://postgrespro.ru/docs/postgrespro/14/errcodes-appendix
-- документация BEGIN https://postgrespro.ru/docs/postgrespro/14/sql-begin
-- savepoint https://postgrespro.ru/docs/postgrespro/14/sql-savepoint

-- уровни транзакций 
-- https://postgrespro.ru/docs/postgrespro/14/sql-set-transaction
-- https://postgrespro.ru/docs/postgrespro/14/transaction-iso

--добавили столбец и заполнили
BEGIN;
ALTER TABLE employee
ADD COLUMN salary decimal(12, 2);

UPDATE employee 
SET salary = random() * 100;
COMMIT;

BEGIN;
UPDATE employees
SET salary = salary * 1.5
WHERE salary < 20;

SAVEPOINT increase_salary;

UPDATE employees
SET salary = salary * 0.8
WHERE salary > 80;

COMMIT;

BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
--BEGIN;

CREATE TABLE last_orders_on_discontinued AS
WITH prod_update AS (
	UPDATE products
	SET discontinued = 1
	WHERE units_in_stock < 10
	RETURNING product_id
)
SELECT * FROM order_details
WHERE product_id IN (SELECT product_id FROM prod_update);

--добавили комманду, которая упадет - ошибка в названии таблицы last_orders_on_discontinued_ERROR
--DROP TABLE last_orders_on_discontinued_ERROR;

SAVEPOINT backup; --создали точку сохранения
DELETE FROM order_details
WHERE product_id IN (SELECT product_id FROM last_orders_on_discontinued);
--можем выполнить запрос до это места, проверить удаленные данные и если что-то пошло не так вызвать 
--ROLLBACK;

ROLLBACK TO backup; -- откатываем изменения до точки сохранения

SELECT COUNT(*) FROM order_details;

COMMIT;

SELECT * FROM last_orders_on_discontinued;

DROP TABLE IF EXISTS last_orders_on_discontinued;
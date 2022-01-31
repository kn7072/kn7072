--1. Создайте функцию, которая делает бэкап таблицы customers (копирует все данные в другую таблицу), 
-- предварительно стирая таблицу для бэкапа, если такая уже существует (чтобы в случае многократного запуска таблица для бэкапа перезатиралась).
CREATE OR REPLACE FUNCTION backup_customers() RETURNS void AS $$
DECLARE
	backup_customers text;
BEGIN
	DROP TABLE IF EXISTS backup_customers;
	 
	SELECT * 
	INTO backup_customers
	FROM customers;
END;
$$ LANGUAGE plpgsql;--SQL ;

CREATE OR REPLACE FUNCTION backup_customers() RETURNS void AS $$
	DROP TABLE IF EXISTS backup_customers;
	SELECT * 
	INTO backup_customers
	FROM customers;
$$ LANGUAGE SQL;

SELECT backup_customers();
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM backup_customers;
--1. Создайте функцию, которая делает бэкап таблицы customers (копирует все данные в другую таблицу), 
-- предварительно стирая таблицу для бэкапа, если такая уже существует (чтобы в случае многократного запуска таблица для бэкапа перезатиралась).
-- CREATE OR REPLACE FUNCTION backup_customers() RETURNS void AS $$
-- DECLARE
-- 	backup_customers text;
-- BEGIN
-- 	DROP TABLE IF EXISTS backup_customers;
	 
-- 	SELECT * 
-- 	INTO backup_customers
-- 	FROM customers;
-- END;
-- $$ LANGUAGE plpgsql;--SQL ;

CREATE OR REPLACE FUNCTION backup_customers() RETURNS void AS $$
	DROP TABLE IF EXISTS backup_customers;
	SELECT * 
	INTO backup_customers
	FROM customers;
$$ LANGUAGE SQL;

SELECT backup_customers();
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM backup_customers;

--2. Создать функцию, которая возвращает средний фрахт (freight) по всем заказам
CREATE OR REPLACE FUNCTION get_freight() RETURNS double precision AS $$
BEGIN
	RETURN AVG(freight) FROM orders;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_freight_sql() RETURNS double precision AS $$
	SELECT AVG(freight) FROM orders;
$$ LANGUAGE SQL;

SELECT get_freight();
SELECT get_freight_sql();

--3. Написать функцию, которая принимает два целочисленных параметра, используемых как нижняя и верхняя границы для генерации случайного числа
--в пределах этой границы (включая сами граничные значения).
--Функция random генерирует вещественное число от 0 до 1.
--Необходимо вычислить разницу между границами и прибавить единицу.
--На полученное число умножить результат функции random() и прибавить к результату значение нижней границы.
--Применить функцию floor() к конечному результату, чтобы не "уехать" за границу и получить целое число.
CREATE OR REPLACE FUNCTION function_1(low int, high int) RETURNS double precision AS $$
DECLARE
	result double precision = 0;
BEGIN
	result := low + ((high - low) + 1) * random();
	RETURN floor(result);
END;
$$ LANGUAGE plpgsql;

SELECT function_1(2, 10);

--4. Создать функцию, которая возвращает самые низкую и высокую зарплаты среди сотрудников заданного города
SELECT * FROM employees
LIMIT 10;

ALTER TABLE employees
ADD COLUMN salary numeric CONSTRAINT CHK_eployees_salary CHECK (salary > 0);

ALTER TABLE employees
ALTER COLUMN salary SET DATA TYPE numeric(8, 2);

UPDATE employees
SET salary = random() * 1000000;

ALTER TABLE employees
ALTER COLUMN salary SET NOT NULL;

DROP FUNCTION IF EXISTS get_low_high_salary(varchar(10));
CREATE OR REPLACE FUNCTION get_low_high_salary(city_var varchar(10), OUT low_salary varchar(4), OUT high_salary varchar(4)) AS $$
BEGIN
	SELECT MIN(extension), MAX(extension)
	FROM employees
	WHERE city = city_var;
END;
$$ LANGUAGE plpgsql;

SELECT get_low_high_salary('Seattle');
SELECT * FROM get_low_high_salary('Seattle');



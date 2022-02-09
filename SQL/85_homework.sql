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
	--SELECT * INTO backup_customers FROM customers;
	CREATE TABLE backup_customers AS 
	SELECT * FROM customers;
$$ LANGUAGE SQL;

SELECT backup_customers();
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM backup_customers;

--2. Создать функцию, которая возвращает средний фрахт (freight) по всем заказам
CREATE OR REPLACE FUNCTION get_freight() RETURNS float8 AS $$
BEGIN
	RETURN AVG(freight) FROM orders;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_freight_sql() RETURNS float8 AS $$
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

SELECT function_1(2, 10) FROM generate_series(1, 10);

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
CREATE OR REPLACE FUNCTION get_low_high_salary(city_var varchar(10), OUT low_salary numeric, OUT high_salary numeric) AS $$
BEGIN
	SELECT MIN(salary), MAX(salary)
	FROM employees
	WHERE city = city_var
	INTO low_salary, high_salary;
END;
$$ LANGUAGE plpgsql;

SELECT salary FROM employees
LIMIT 3;

SELECT get_low_high_salary('Seattle');
SELECT * FROM get_low_high_salary('Seattle');

--5. Создать функцию, которая корректирует зарплату на заданный процент,  но не корректирует зарплату, 
--если её уровень превышает заданный уровень при этом верхний уровень зарплаты по умолчанию равен 70, а процент коррекции равен 15%. 
CREATE OR REPLACE FUNCTION up_salary() RETURNS void AS $$
DECLARE
	avg_salary numeric := (SELECT AVG(salary) FROM employees);
BEGIN
	UPDATE employees
	SET salary = salary * 1.15
	WHERE salary < avg_salary;
END;
$$ LANGUAGE plpgsql;

SELECT MIN(salary) FROM employees;

SELECT up_salary();

--6. Модифицировать функцию, корректирующую зарплату таким образом, чтобы в результате коррекции, она так же выводила бы изменённые записи.
DROP FUNCTION IF EXISTS up_salary_and_get_data;
CREATE OR REPLACE FUNCTION up_salary_and_get_data() RETURNS SETOF employees AS $$
DECLARE
	avg_salary numeric := (SELECT AVG(salary) FROM employees);
BEGIN
	UPDATE employees
	SET salary = salary * 1.15
	WHERE salary < avg_salary
	RETURNING employees;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION up_salary_and_get_data() RETURNS SETOF employees AS $$
	UPDATE employees
	SET salary = salary * 1.15
	WHERE salary < (SELECT AVG(salary) FROM employees)
	RETURNING *; --возвращаем измененные строки
$$ LANGUAGE SQL;

SELECT last_name, salary FROM employees
ORDER BY salary
LIMIT 3;

SELECT last_name, salary FROM up_salary_and_get_data()
ORDER BY salary
LIMIT 3;

--7. Модифицировать предыдущую функцию так, чтобы она возвращала только колонки last_name, first_name, title, salary
CREATE OR REPLACE FUNCTION up_salary_and_get_data_2() RETURNS TABLE(last_name text, first_name text, title text, salary numeric) AS $$
	UPDATE employees
	SET salary = salary * 1.15
	WHERE salary < (SELECT AVG(salary) FROM employees)
	RETURNING last_name, first_name, title, salary; --возвращаем необходимые столбцы
$$ LANGUAGE SQL;

SELECT * FROM up_salary_and_get_data_2()
ORDER BY salary
LIMIT 3

--8. Написать функцию, которая принимает метод доставки и возвращает записи из таблицы orders в которых freight меньше значения, определяемого по следующему алгоритму:
--- ищем максимум фрахта (freight) среди заказов по заданному методу доставки
--- корректируем найденный максимум на 30% в сторону понижения
--- вычисляем среднее значение фрахта среди заказов по заданному методому доставки
--- вычисляем среднее значение между средним найденным на предыдущем шаге и скорректированным максимумом
--- возвращаем все заказы в которых значение фрахта меньше найденного на предыдущем шаге среднего
DROP FUNCTION IF EXISTS get_orders_by_shipping;
CREATE OR REPLACE FUNCTION get_orders_by_shipping(ship_method int) RETURNS SETOF orders AS $$
DECLARE
	average numeric;
	maximum numeric;
	middle numeric;
BEGIN
	SELECT MAX(freight), AVG(freight) INTO maximum, average
	FROM orders
	WHERE ship_method = ship_via;
	
	maximum := maximum - (maximum * 0.3);
	middle := (maximum + average) / 2;
	
	RETURN QUERY
	SELECT *
	FROM orders
	WHERE freight < middle;
END;
$$ LANGUAGE plpgsql;

SELECT DISTINCT ship_via  FROM orders;
SELECT COUNT(*) FROM get_orders_by_shipping(2);

--9. Написать функцию, которая принимает:
--уровень зарплаты, максимальную зарплату (по умолчанию 80) минимальную зарплату (по умолчанию 30), коээфициет роста зарплаты (по умолчанию 20%)
--Если зарплата выше минимальной, то возвращает false
--Если зарплата ниже минимальной, то увеличивает зарплату на коэффициент роста и проверяет не станет ли зарплата после повышения превышать максимальную.
--Если превысит - возвращает false, в противном случае true.
--Проверить реализацию, передавая следующие параметры
--(где c - уровень з/п, max - макс. уровень з/п, min - минимальный уровень з/п, r - коэффициент):
--c = 40, max = 80, min = 30, r = 0.2 - должна вернуть false
--c = 79, max = 81, min = 80, r = 0.2 - должна вернуть false
--c = 79, max = 95, min = 80, r = 0.2 - должна вернуть true
CREATE OR REPLACE FUNCTION should_increase_salary(
	cur_salary numeric,
	max_salary numeric DEFAULT 80,
	mim_salary numeric DEFAULT 30,
	increase_rate numeric DEFAULT 0.2
) RETURNS bool AS
$$
DECLARE
	new_salary numeric;
BEGIN
	IF cur_salary >= max_salary OR cur_salary >= min_salary THEN
		RETURN false;
	END IF;
	
	IF cur_salary < min_salary THEN
		new_salary = cur_salary + (cur_salary * increase_rate);
	END IF;
	
	IF new_salary > max_salary THEN
		RETURN false;
	ELSE
		RETURN true;
	END IF;
END;
$$ LANGUAGE plpgsql;

SELECT should_increase_salary(40, 80, 30, 0.2);






ALTER TABLE customers
ADD COLUMN last_updated timestamp;

CREATE OR REPLACE FUNCTION track_changes_on_customers() RETURNS trigger AS $$
BEGIN
	NEW.last_updated = now();
	RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS customers_timestamp ON customers;
CREATE TRIGGER customers_timestamp BEFORE INSERT OR UPDATE ON customers
	FOR EACH ROW EXECUTE PROCEDURE track_changes_on_customers();

SELECT * 
FROM customers
WHERE customer_id = 'ALFKI';

-- срабатывает триггер (UPDATE)
UPDATE customers
SET address = 'bla'
WHERE customer_id = 'ALFKI';

-- срабатывает триггер (INSERT)
INSERT INTO customers
VALUES ('ABCDE', 'company', 'contact', 'title', 'address', 'city', null, 'code', 'country', '', '', null);

-----------------
ALTER TABLE employees
ADD COLUMN user_changed text;

CREATE OR REPLACE FUNCTION track_changes_on_employees() RETURNS trigger AS $$
BEGIN
	-- session_user https://postgrespro.ru/docs/postgrespro/14/functions-info
	-- Выдаёт имя пользователя сеанса.
	NEW.user_changed = session_user;
	RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS employees_user_change ON employees;
CREATE TRIGGER employees_user_change BEFORE INSERT OR UPDATE ON employees
	FOR EACH ROW EXECUTE PROCEDURE track_changes_on_employees();
	
SELECT * FROM employees;

-- если отсутствует колонка salary
ALTER TABLE employees
ADD COLUMN salary decimal(12, 2);

UPDATE employees
SET salary = random() * 100;
--

UPDATE employees
SET salary = 100
WHERE employee_id = 1;

INSERT INTO employees
VALUES (10, '', '', '', '', null, null, '', '', '', '', '', '', '',   'fff', 'fff', null, 'fff', 1000, '');


DROP TYPE IF EXISTS price_bounds CASCADE;
CREATE TYPE price_bounds AS (
	min_price numeric,
	max_price numeric
);

create or replace function get_salary_boundaries_by_city(emp_city varchar) RETURNS SETOF price_bounds AS 
$$
	SELECT MIN(salary), MAX(salary)
  	FROM employees
	WHERE city = emp_city
$$ language sql;

SELECT city FROM employees;
SELECT get_salary_boundaries_by_city('Seattle');

--2
--Создать перечисление армейских званий США, включающее следующие значения: Private, Corporal, Sergeant
--Вывести все значения из перечисления.
--Добавить значение Major после Sergeant в перечисление
--Создать таблицу личного состава с колонками: person_id, first_name, last_name, person_rank (типа перечисления)
--Добавить несколько записей, вывести все записи из таблицы

CREATE TYPE army_usa AS ENUM
('Private', 'Corporal', 'Sergeant');

SELECT enum_range(null::chess_title);

ALTER TYPE army_usa
ADD VALUE 'Major' BEFORE 'Sergeant';

DROP TABLE IF EXISTS persons;
CREATE TABLE IF NOT EXISTS persons (
	person_id serial PRIMARY KEY,
	first_name varchar,
	last_name varchar,
	person_rank army_usa
);

INSERT INTO persons(first_name, last_name, person_rank)
VALUES
('a', 'b', 'Private');

SELECT * FROM persons;
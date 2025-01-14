DROP TABLE IF EXISTS agent;
DROP DOMAIN IF EXISTS text_no_space_null;
CREATE DOMAIN text_no_space_null AS TEXT NOT NULL CHECK (value ~ '^(?!\s*$).+');

CREATE TABLE agent(
	first_name text_no_space_null,
	last_name text_no_space_null
);

INSERT INTO agent
VALUES ('bob', 'taylor');

INSERT INTO agent
VALUES ('bob 123', 'taylor');

SELECT * FROM agent;

INSERT INTO agent
VALUES ('', 'taylor');

INSERT INTO agent
VALUES (NULL, 'taylor');

INSERT INTO agent
VALUES ('   ', 'taylor');

--добавим новое ограничение на domain
ALTER DOMAIN text_no_space_null ADD CONSTRAINT text_no_space_null_length32 CHECK (length(value) <= 32) NOT VALID; --NOT VALID чтобы ограничение не ругалось на данные, которые уже существуют в таблицах
--удаляем ограничение
ALTER DOMAIN text_no_space_null DROP CONSTRAINT text_no_space_null_length32;

INSERT INTO agent
VALUES (11111111111111111111111111111111111111111111111111111111111111111, 'taylor');

--чтобы проверить есть ли ошибки
ALTER DOMAIN text_no_space_null VALIDATE CONSTRAINT text_no_space_null_length32;

--почистим таблицу, чтобы соответствовать ограничению
DELETE FROM agent
WHERE length(first_name) > 32;

--109 составные типы
--вместо соствавных типов обычно предпочитают таблицы так как составные типы не поддерживают constraint
DROP FUNCTION IF EXISTS get_price_boundaries;
CREATE OR REPLACE FUNCTION get_price_boundaries(OUT max_price real, OUT min_price real) AS $$
	SELECT MAX(unit_price), min(unit_price)
	FROM products
$$ LANGUAGE SQL;

SELECT * FROM get_price_boundaries();

CREATE TYPE price_bounds AS (
	max_price real,
	min_price real
);

CREATE OR REPLACE FUNCTION get_price_boundaries_2() RETURNS SETOF price_bounds AS $$
	SELECT MAX(unit_price), min(unit_price)
	FROM products
$$ LANGUAGE SQL;

SELECT * FROM get_price_boundaries_2();

--создадим тип комплексных чисел
CREATE TYPE complex AS (
	r float8,
	i float8
);

CREATE TABLE math_calcs (
	math_id serial,
	val complex
);

INSERT INTO math_calcs(val)
VALUES 
(ROW(3.0, 4.0)),
(ROW(2.0, 1.0));

SELECT * FROM math_calcs;

SELECT (val).r FROM math_calcs; --обращаемся к полю r составного типа complex
--или дополнительно указать название таблицы на случай сложных запросов
SELECT (math_calcs.val).r FROM math_calcs;

SELECT (val).* FROM math_calcs; --забираем все данные из колонки составного типа

--обновление значений составного типа
UPDATE math_calcs
SET val = ROW(5.0, 4.0) --переписываем все значение составного типа
WHERE math_id = 1;

UPDATE math_calcs
SET val.r = 3.0 --обновляем только поле r
WHERE math_id = 1;

UPDATE math_calcs
SET val.r = (val).r + 1.0 --обновляем только поле r, увеличиваем на 1
WHERE math_id = 1;
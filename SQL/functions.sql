--https://postgrespro.ru/docs/postgrespro/14/xfunc-sql
--36.5.3. Функции SQL со сложными типами
CREATE TABLE emp (
    name        text,
    salary      numeric,
    age         integer,
    cubicle     point
);

INSERT INTO emp
VALUES
('1', 1, 1, point(1,1));

SELECT * FROM emp;

--возможно создать функцию, возвращающую составной тип. 
--Например, эта функция возвращает одну строку emp:
CREATE FUNCTION new_emp() RETURNS emp AS $$
	SELECT text 'None' AS name,
		   1000.0 AS salary,
		   25 AS age,
		   point '(2,2)' AS cubicle;
$$ LANGUAGE SQL;

-- или

CREATE OR REPLACE FUNCTION new_emp() RETURNS emp AS $$
    SELECT ROW('None', 1000.0, 25, '(2,2)')::emp;
$$ LANGUAGE SQL;

SELECT new_emp();
--Когда используется функция, возвращающая составной тип, может возникнуть желание получить из её результата только одно поле (атрибут).
--Это можно сделать, применяя такую запись: 
SELECT (new_emp()).salary;

--36.5.8. Функции SQL, порождающие таблицы
CREATE TABLE foo (fooid int, foosubid int, fooname text);
INSERT INTO foo VALUES (1, 1, 'Joe');
INSERT INTO foo VALUES (1, 2, 'Ed');
INSERT INTO foo VALUES (2, 1, 'Mary');

DROP FUNCTION IF EXISTS getfoo;
CREATE OR REPLACE FUNCTION getfoo(int) RETURNS foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT *, upper(fooname) FROM getfoo(1) AS t1;

--36.5.9. Функции SQL, возвращающие множества
CREATE FUNCTION getfoo(int) RETURNS SETOF foo AS $$
    SELECT * FROM foo WHERE fooid = $1;
$$ LANGUAGE SQL;

SELECT * FROM getfoo(1) AS t1;

--Также возможно выдать несколько строк со столбцами, определяемыми выходными параметрами, 
-- следующим образом: 
CREATE TABLE tab (y int, z int);
INSERT INTO tab VALUES (1, 2), (3, 4), (5, 6), (7, 8);

--Здесь ключевая особенность заключается в записи RETURNS SETOF record, показывающей, 
-- что функция возвращает множество строк вместо одной. Если существует только один выходной параметр,
-- укажите тип этого параметра вместо record.
CREATE FUNCTION sum_n_product_with_tab (x int, OUT sum int, OUT product int)
RETURNS SETOF record
AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;

SELECT * FROM sum_n_product_with_tab(10);

--36.5.10. Функции SQL, возвращающие таблицы (TABLE)
--Есть ещё один способ объявить функцию, возвращающую множества, — использовать синтаксис RETURNS TABLE(столбцы). 
--Это равнозначно использованию одного или нескольких параметров OUT с объявлением функции как возвращающей SETOF record 
--(или SETOF тип единственного параметра, если это применимо). Этот синтаксис описан в последних версиях стандарта SQL, 
--так что этот вариант может быть более портируемым, чем SETOF.

--Например, предыдущий пример с суммой и произведением можно также переписать так: 
CREATE FUNCTION sum_n_product_with_tab (x int) RETURNS TABLE(sum int, product int) AS $$
    SELECT $1 + tab.y, $1 * tab.y FROM tab;
$$ LANGUAGE SQL;
--Запись RETURNS TABLE не позволяет явно указывать OUT и INOUT для параметров — 
-- все выходные столбцы необходимо записать в списке TABLE.




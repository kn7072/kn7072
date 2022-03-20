-- https://itdoxy.com/%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80-postgresql-select-distinct/
CREATE TABLE IF NOT EXISTS t1 (
	id serial NOT NULL PRIMARY KEY,
	bcolor VARCHAR,
	fcolor VARCHAR
);

INSERT INTO t1 (bcolor, fcolor)
VALUES
  ('red', 'red'),
  ('red', 'red'),
  ('red', NULL),
  (NULL, 'red'),
  ('red', 'green'),
  ('red', 'blue'),
  ('green', 'red'),
  ('green', 'blue'),
  ('green', 'green'),
  ('blue', 'red'),
  ('blue', 'green'),
  ('blue', 'blue');
  
SELECT id, bcolor, fcolor
FROM t1;

--PostgreSQL DISTINCT на примере одного столбца
--Запрос возвращает уникальную комбинацию bcolor и fcolor из таблицы t1. 
SELECT DISTINCT bcolor
FROM t1
ORDER BY bcolor;

--PostgreSQL DISTINCT на примере нескольких столбцов
SELECT DISTINCT bcolor, fcolor
FROM t1
ORDER BY bcolor, fcolor;

--Пример PostgreSQL DISTINCT ON
--Следующая инструкция сортирует набор результатов по bcolor и fcolor, 
--а затем для каждой группы дубликатов сохраняет первую строку в возвращенном наборе результатов.
SELECT DISTINCT ON (bcolor) bcolor, fcolor
FROM t1
ORDER BY bcolor, fcolor;
--Индекс - структура данных, ускоряющая выборку данных из таблицы.
-- индекс - объект базы данный, позволяет искать значения без полного перебора
-- индекс устанавливает соответствие между ключом(значение проиндексированного столбца) и строками таблицы в которох этот ключ встречается
-- по primary key и unique столбцам индексы создаются автоматически - B-tree деревья

--ps auxw |  grep postgres | grep -- -D
-- из вывода команды выше видим где находится база и конфиг
-- данные базы находятся /var/lib/postgresql/[version]/main/data/
-- config_file=/etc/postgresql/12/main/postgresql.conf

--https://postgrespro.ru/docs/postgrespro/14/catalog-pg-am
SELECT amname FROM pg_am; -- доступные типы индексов

--https://postgrespro.ru/docs/postgrespro/14/catalogs
SELECT * FROM pg_tables;

--97 лекция
CREATE TABLE perf_test(
	id int,
	reason text COLLATE "C", -- https://postgrespro.ru/docs/postgrespro/14/sql-createtable
	--COLLATE правило_сортировки
    --Предложение COLLATE назначает правило сортировки для столбца (который должен иметь тип, поддерживающий сортировку). 
	--Если оно отсутствует, используется правило сортировки по умолчанию, установленное для типа данных столбца.
	annotation text COLLATE "C"
);

INSERT INTO perf_test
SELECT s.id, md5(random()::text), NULL
FROM generate_series(1, 10000000) AS s(id) --https://postgrespro.ru/docs/postgrespro/14/functions-srf
ORDER BY random();

UPDATE perf_test
SET annotation = UPPER(md5(random()::text));

EXPLAIN
SELECT *
FROM perf_test
WHERE id = 3700000;

--создаем индекс
CREATE INDEX idx_perf_text_id ON perf_test(id);

EXPLAIN ANALYZE --запрос будет выполнен
SELECT *
FROM perf_test
WHERE reason LIKE 'ab%' AND annotation LIKE 'AB%';

--строим индекс по двум столбцам
CREATE INDEX idx_perf_test_reason_annotation ON perf_test(reason, annotation);

EXPLAIN
SELECT *
FROM perf_test
WHERE reason LIKE 'ab%' AND annotation LIKE 'AB%';

EXPLAIN
SELECT *
FROM perf_test
WHERE reason LIKE 'ab%'; -- при поиске по первой колонке(reason), поиск будет использовать индекс созданный по двум колонкам idx_perf_test_reason_annotation


EXPLAIN
SELECT *
FROM perf_test
WHERE annotation LIKE 'ab%'; -- при поиске по второй колонке(annotation), поиск не будет использовать индекс idx_perf_test_reason_annotation,
-- по индексу созданному по двум столбцам можно искать или по первому столбцу или по обоим столцам, но не по второму

EXPLAIN
SELECT *
FROM perf_test
WHERE annotation LIKE 'AB%';

CREATE INDEX idx_perf_test_annotation ON perf_test(annotation);

EXPLAIN
SELECT *
FROM perf_test
WHERE LOWER(annotation) LIKE 'ab%'; --индекс не сработал, так как использовалась функция LOWER, необходим новый индекс

--создаем индекс по выражению
CREATE INDEX idx_perf_test_annotation_lower ON perf_test(LOWER(annotation)); --запрос выше будет использовать этот индекс

--создаем индекс gin -для поиска по строкам
--нет гарантий, что планировщик будет использовать индекс, все зависит от числа записей
EXPLAIN ANALYSE
SELECT COUNT(*)
FROM perf_test
WHERE reason LIKE '%ab%'; --хотя индекс создан(создается ниже), для поиска он не используется, 
--так как подходящих записей слишком много и планировщик решает использовать parallel seq

CREATE EXTENSION pg_trgm; --необходимо подключить расширение
CREATE INDEX trgm_idx_parf_test_reason ON perf_test USING gin (reason gin_trgm_ops);

EXPLAIN ANALYSE
SELECT COUNT(*)
FROM perf_test
WHERE reason LIKE '%abc%'; --тут записей меньше чем в предыдущем запросе и планировщик использует trgm_idx_parf_test_reason
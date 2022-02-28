SELECT *
FROM products;

SELECT supplier_id, SUM(units_in_stock)
FROM products
GROUP BY supplier_id
ORDER BY supplier_id;

SELECT supplier_id, category_id, SUM(units_in_stock)
FROM products
GROUP BY supplier_id, category_id
ORDER BY supplier_id;

--7.2.4. GROUPING SETS, CUBE и ROLLUP
--https://postgrespro.ru/docs/postgrespro/14/queries-table-expressions
--данный запрос эквивалент предыдущих двух
--сразу выводятся результаты группировки как по supplier_id так и по совместной группировке (supplier_id, category_id)
SELECT supplier_id, category_id, SUM(units_in_stock)
FROM products
GROUP BY GROUPING SETS ((supplier_id), (supplier_id, category_id))
ORDER BY supplier_id, category_id NULLS FIRST;

--ROLLUP это сокращение GROUPING SETS
SELECT supplier_id, SUM(units_in_stock)
FROM products
GROUP BY ROLLUP(supplier_id); --выведет дополнительную запись с суммой по всем units_in_stock [null] 3119

SELECT supplier_id, category_id, SUM(units_in_stock)
FROM products
GROUP BY ROLLUP (supplier_id, category_id)
ORDER BY supplier_id, category_id NULLS FIRST;

SELECT supplier_id, category_id, reorder_level, SUM(units_in_stock)
FROM products
GROUP BY ROLLUP (supplier_id, category_id, reorder_level)
ORDER BY supplier_id, category_id, reorder_level NULLS FIRST;

--CUBE почти тоже самое что и ROLLUP только делает больше перестановок
--группировка по supplier_id, (supplier_id, category_id), category_id тоесть по всем возможным комбинациям
SELECT supplier_id, category_id, SUM(units_in_stock)
FROM products
GROUP BY CUBE (supplier_id, category_id)
ORDER BY supplier_id, category_id NULLS FIRST;

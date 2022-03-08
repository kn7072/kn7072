SELECT * FROM products;
--Оконные функции разрешается использовать в запросе только в списке SELECT и предложении ORDER BY. Во всех остальных предложениях, включая GROUP BY, HAVING и WHERE, они запрещены. Это объясняется тем, что логически они выполняются после этих предложений, а также после не оконных агрегатных функций, и значит агрегатную функцию можно вызывать в аргументах оконной, но не наоборот.

--https://postgrespro.ru/docs/postgrespro/14/tutorial-window
--функция rank выдаёт порядковый номер для каждого уникального значения в разделе текущей строки, 
--по которому выполняет сортировку предложение ORDER BY. У функции rank нет параметров, так как её поведение полностью определяется предложением OVER.
SELECT product_name, units_in_stock,
		RANK() OVER(ORDER BY product_id)--product_id имеет уникальное значение для каждой записи, поэтому и RANK() выдает уникальные значения
FROM products;

SELECT product_name, units_in_stock,
	RANK() OVER(ORDER BY units_in_stock) --units_in_stock не уникальные значения, RANK() будет выдавать повторяющиеся значения для одинаковых units_in_stock
	--данные будут выводиться с гэпом - когда идут несколько одинановых значение, а потом число(одинаковых значений) приплюсовывается, образуя гэп
FROM products;

SELECT product_name, units_in_stock,
	DENSE_RANK() OVER(ORDER BY units_in_stock) --units_in_stock не уникальные значения, DENSE_RANK() будет выдавать повторяющиеся значения для одинаковых units_in_stock
	--но гэпа не будет
FROM products;

SELECT product_name, unit_price,
	DENSE_RANK() OVER(
		ORDER BY
			CASE
				WHEN unit_price > 80 THEN 1
				WHEN unit_price > 30 AND unit_price < 80 THEN 2
				ELSE 3
			END
	) AS ranking
FROM products	
ORDER BY unit_price DESC;

--хотим посмотреть отличие текущей цены от предыдущей
SELECT product_name, unit_price,
	LAG(unit_price) OVER(ORDER BY unit_price DESC) - unit_price AS price_lag
FROM products	
ORDER BY unit_price DESC;

--хотим посмотреть отличие текущей цены от следующей
SELECT product_name, unit_price,
	LEAD(unit_price) OVER(ORDER BY unit_price) - unit_price AS price_lag
FROM products	
ORDER BY unit_price;
	
--хотим посмотреть отличие текущей цены от следующей на 2 (LEAD(unit_price, 2))
SELECT product_name, unit_price,
	LEAD(unit_price, 2) OVER(ORDER BY unit_price) - unit_price AS price_lag
FROM products	
ORDER BY unit_price;	

--Когда в запросе вычисляются несколько оконных функций для одинаково определённых окон, конечно можно написать для каждой из них отдельное предложение OVER, но при этом оно будет дублироваться, что неизбежно будет провоцировать ошибки. Поэтому лучше определение окна выделить в предложение WINDOW, а затем ссылаться на него в OVER. Например: 
SELECT sum(salary) OVER w, avg(salary) OVER w
  FROM empsalary
  WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);

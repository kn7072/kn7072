CREATE OR REPLACE FUNCTION get_product_price_by_name(prod_name varchar) RETURNS real AS $$
	SELECT unit_price
	FROM products
	WHERE product_name = prod_name
$$ LANGUAGE SQL;

SELECT get_product_price_by_name('Chocolade') AS chocolate_price;

SELECT *
FROM products;

CREATE OR REPLACE FUNCTION get_price_boundaies_by_discontinuity(is_discontinued int DEFAULT 1, OUT max_price real, OUT min_price real) AS $$
	SELECT MAX(unit_price), MIN(unit_price)
	FROM products
	WHERE discontinued = is_discontinued
$$ LANGUAGE SQL;

--возвращает record
SELECT get_price_boundaies_by_discontinuity(1);

--значения по столбцам
SELECT * FROM get_price_boundaies_by_discontinuity(0);

--is_discontinued по умолчанию 1
SELECT * FROM get_price_boundaies_by_discontinuity();

--78
--DROP FUNCTION get_avereage_prices_by_prod_categories
CREATE OR REPLACE FUNCTION get_avereage_prices_by_prod_categories()
		RETURNS SETOF double precision AS $$
	SELECT AVG(unit_price)
	FROM products
	GROUP BY category_id
$$ LANGUAGE SQL;

SELECT * FROM get_avereage_prices_by_prod_categories() AS average_prices;

CREATE OR REPLACE FUNCTION get_avg_prices_by_prod_cats(OUT sum_price real, OUT avg_price float8)
		RETURNS SETOF RECORD AS $$
	SELECT SUM(unit_price), AVG(unit_price)	
	FROM products
	GROUP BY category_id	
$$ LANGUAGE SQL;

SELECT sum_price FROM get_avg_prices_by_prod_cats();
SELECT sum_price, avg_price FROM get_avg_prices_by_prod_cats();
SELECT sum_price AS sum_of, avg_price AS in_avg FROM get_avg_prices_by_prod_cats();

-- в фунции не указаны возвращаемые поля, только RECORD - по возможности таких определений стоит избегать
DROP FUNCTION get_avg_prices_by_prod_cats;
CREATE OR REPLACE FUNCTION get_avg_prices_by_prod_cats()
		RETURNS SETOF RECORD AS $$
	SELECT SUM(unit_price), AVG(unit_price)	
	FROM products
	GROUP BY category_id	
$$ LANGUAGE SQL;

SELECT sum_price FROM get_avg_prices_by_prod_cats(); -- НЕ СРАБОТАЕТ
SELECT sum_price, avg_price FROM get_avg_prices_by_prod_cats(); -- НЕ СРАБОТАЕТ
SELECT sum_price AS sum_of, avg_price AS in_avg FROM get_avg_prices_by_prod_cats(); -- НЕ СРАБОТАЕТ
SELECT * FROM get_avg_prices_by_prod_cats(); -- НЕ СРАБОТАЕТ
SELECT * FROM get_avg_prices_by_prod_cats() AS (sum_price real, avg_price float8); -- требуется ясно указать имена столбцов и типы

--
CREATE OR REPLACE FUNCTION get_customers_by_country(customer_country varchar)
		RETURNS TABLE(char_code char, company_name varchar) AS $$
	SELECT customer_id, company_name
	FROM customers
	WHERE country = customer_country
$$ LANGUAGE SQL;

SELECT * FROM get_customers_by_country('USA');
SELECT company_name FROM get_customers_by_country('USA');

--
DROP FUNCTION get_customers_by_country;
CREATE OR REPLACE FUNCTION get_customers_by_country(customer_country varchar)
		RETURNS SETOF customers AS $$
	SELECT * --обязательно нужно возвращать все столбцы * так как RETURNS SETOF customers
	FROM customers
	WHERE country = customer_country
$$ LANGUAGE SQL;

SELECT * FROM get_customers_by_country('USA');
SELECT company_name FROM get_customers_by_country('USA');
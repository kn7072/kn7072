SELECT *
FROM customers;

--создаем эксперементальную таблицу
SELECT *
INTO tmp_customers
FROM customers;

UPDATE tmp_customers
SET region = 'unknown'
WHERE region IS NULL;

CREATE OR REPLACE FUNCTION fix_customer_region() RETURNS void AS $$
	UPDATE tmp_customers
	SET region = 'unknown'
	WHERE region IS NULL;
$$ language SQL;

SELECT fix_customer_region();

SELECT *
FROM tmp_customers;

CREATE OR REPLACE FUNCTION get_total_number_of_goods() RETURNS bigint AS $$
	SELECT SUM(units_in_stock)
	FROM products
$$ language SQL;

SELECT get_total_number_of_goods() AS goods;

CREATE OR REPLACE FUNCTION get_avg_price() RETURNS float8 AS $$
	SELECT AVG(unit_price)
	FROM products
$$ language SQL;

SELECT get_avg_price() AS avg_price;


	
--plpgsql

CREATE OR REPLACE FUNCTION get_total_of_goods() RETURNS bigint AS $$
BEGIN
	RETURN sum(units_in_stock) --RETURN обязателен
	FROM products; --; обязательна
END;
$$ LANGUAGE plpgsql;

SELECT get_total_of_goods();

CREATE OR REPLACE FUNCTION get_max_price_from_discontinued() RETURNS real AS $$
BEGIN
	RETURN max(unit_price) --RETURN обязателен
	FROM products
	WHERE discontinued = 1; --; обязательна
END;
$$ LANGUAGE plpgsql;

SELECT get_max_price_from_discontinued();

CREATE OR REPLACE FUNCTION get_price_boundaries(OUT max_price real, OUT min_price real) AS $$
BEGIN
	--max_price := MAX(unit_price) FROM products;
	--min_price := MIN(unit_price) FROM products;
	SELECT MAX(unit_price), MIN(unit_price)
	--INTO max_price, min_price
	FROM products;
END;
$$ LANGUAGE plpgsql;

SELECT get_price_boundaries();
SELECT * FROM get_price_boundaries();


CREATE OR REPLACE FUNCTION get_sum(x int, y int, out result int) AS $$
BEGIN
	result := x + y; -- или result = x + y;  (:= чтобы не пуать с сравнением)
	RETURN; --чтобы принудительно завершить функцию
END
$$ LANGUAGE plpgsql;

SELECT * FROM get_sum(2, 3);

DROP FUNCTION IF EXISTS get_customers_by_country;
CREATE OR REPLACE FUNCTION get_customers_by_country(customer_country varchar) RETURNS SETOF customers AS $$
BEGIN
	RETURN QUERY --потому что RETURNS SETOF customers
	SELECT *
	FROM customers
	WHERE country = customer_country;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_customers_by_country('USA');




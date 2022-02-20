CREATE OR REPLACE FUNCTION get_avg(VARIADIC country_list text[]) RETURNS float8 AS $$
--BEGIN
	SELECT AVG(freight)
	FROM orders
	WHERE ship_country = ANY(country_list);
	--GROUP BY ship_country;
--END;
$$ LANGUAGE SQL;

SELECT DISTINCT ship_country
FROM orders;

SELECT get_avg('USA', 'Spain', 'Italy');
SELECT get_avg(VARIADIC ARRAY['USA', 'Spain', 'Italy']);

DROP FUNCTION IF EXISTS get_avg_plpgsql;
CREATE OR REPLACE FUNCTION get_avg_plpgsql(VARIADIC country_list text[]) RETURNS TABLE(country varchar, avg_freight double precision) AS $$
BEGIN
	RETURN QUERY
	SELECT ship_country, AVG(freight)-- INTO temp_result
	FROM orders
	WHERE ship_country = ANY(country_list)
	GROUP BY ship_country;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_avg_plpgsql('USA', 'Spain', 'Italy');
SELECT get_avg_plpgsql(VARIADIC ARRAY['USA', 'Spain', 'Italy']);

--106
CREATE OR REPLACE FUNCTION check_phone_number(code int, VARIADIC list_numbers text[]) RETURNS SETOF text AS $$
DECLARE
	number_i text;
BEGIN
	FOREACH number_i IN ARRAY list_numbers
	LOOP
		RAISE NOTICE 'cur val is %', number_i;
		CONTINUE WHEN number_i NOT LIKE CONCAT('__(', code, ')%');  --пропускаем если номер не подходит по маске
		RETURN NEXT number_i;
	END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM check_phone_number(903, '+7(903)000', '+7(111)111', '+7(903)222');
SELECT * FROM check_phone_number(903, VARIADIC ARRAY['+7(903)000', '+7(111)111', '+7(903)222']);


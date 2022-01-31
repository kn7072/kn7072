CREATE OR REPLACE FUNCTION get_square(ab real, bc real, ac real) RETURNS real AS $$
DECLARE
	perimetr real;
BEGIN
	perimetr = (ab + bc + ac) / 2;
	RETURN sqrt(perimetr * (perimetr - ab) * (perimetr - bc) * (perimetr - ac));

END;
$$ LANGUAGE plpgsql;

SELECT get_square(2, 2, 2);

CREATE OR REPLACE FUNCTION calc_middle_price() RETURNS SETOF products AS $$
DECLARE
	avg_price real;
	low_price real;
	high_price real;
BEGIN
	SELECT AVG(unit_price) INTO avg_price --INTO avg_price, присваевает результат SELECT переменной avg_price
	FROM products;
	low_price = avg_price * 0.75;
	high_price = avg_price * 1.75;
	
	RETURN QUERY
	SELECT * FROM products
	WHERE unit_price BETWEEN low_price AND high_price;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM calc_middle_price();

--82
CREATE FUNCTION convert_temp_to(temperature real, to_celsius bool DEFAULT true) RETURNS real AS $$
DECLARE
	result_temp real;
BEGIN
	IF to_celsius THEN
		result_temp = (5.0 / 9.0) * (temperature - 32);
	ELSE
		result_temp = (9.0 / 5.0) * temperature + 32;
	END IF;
	RETURN result_temp;
END;
$$ LANGUAGE plpgsql;

SELECT convert_temp_to(80);
SELECT convert_temp_to(26.7, false);

CREATE FUNCTION get_season(month_number int) RETURNS text AS $$
DECLARE
	season text;
BEGIN
	IF month_number BETWEEN 3 AND 5 THEN
		season = 'Spring';
	ELSEIF month_number BETWEEN 6 AND 8 THEN
		season = 'Summer';
	ELSEIF month_number BETWEEN 9 AND 11 THEN
		season = 'Autum';	
	ELSE
		season = 'Winter';
	END IF;
	
	RETURN season;
END;
$$ LANGUAGE plpgsql;

SELECT get_season(2);
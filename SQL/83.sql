CREATE OR REPLACE FUNCTION fib(n int) RETURNS int AS $$
DECLARE 
	counter int = 0;
	i int = 0;
	j int = 1;
BEGIN
	IF n < 1 THEN
		RETURN 0;
	END IF;
	
	WHILE counter < n
	LOOP
		counter = counter + 1;
		SELECT j, i + j INTO i, j;	
	END LOOP;
	
	RETURN i;
END;
$$ LANGUAGE plpgsql;

SELECT fib(5);

--------------------------------------------------------------
-- EXIT WHEN
CREATE OR REPLACE FUNCTION fib(n int) RETURNS int AS $$
DECLARE 
	counter int = 0;
	i int = 0;
	j int = 1;
BEGIN
	IF n < 1 THEN
		RETURN 0;
	END IF;
	LOOP
		EXIT WHEN counter > n; --выходим если условие выполняется
		counter = counter + 1;
		SELECT j, i + j INTO i, j;	
	END LOOP;
	
	RETURN i;
END;
$$ LANGUAGE plpgsql;

SELECT fib(5);

--------------------------------------------------------------
--ананимный блок кода
DO $$
BEGIN
	FOR counter IN 1..5
	-- FOR counter IN 1..10 BY 2 -- итерации с шагом 2
	-- FOR counter IN REVERSE 5..1 --в обратном порядке
	LOOP
		RAISE NOTICE 'Counter: %s', counter;
	END LOOP;
END$$;

--------------------------------------------------------------
-- RETURN NEXT --накапливает значения в результирующем наборе
CREATE FUNCTION return_ints() RETURNS SETOF int AS $$
BEGIN
	RETURN NEXT 1;
	RETURN NEXT 2;
	RETURN NEXT 3;
	--RETURN
END;
$$ LANGUAGE plpgsql;

SELECT * FROM return_ints();

CREATE FUNCTION after_christmas_sale() RETURNS SETOF products AS $$
DECLARE
	product record;
BEGIN
	FOR product IN SELECT * FROM products
	LOOP
		IF product.category_id IN (1, 4, 8) THEN
			product.unit_price = product.unit_price * 0.8;
		ELSEIF product.category_id IN (2, 3, 7) THEN
			product.unit_price = product.unit_price * 0.75;
		ELSE
			product.unit_price = product.unit_price * 1.1;
		END IF;
		RETURN NEXT product;
	END LOOP;	
END;
$$ LANGUAGE plpgsql;

SELECT * FROM after_christmas_sale();

--Приведение типов

CREATE OR REPLACE FUNCTION type_testing(money_val float8) RETURNS void AS $$
BEGIN
	RAISE NOTICE 'ran %', money_val;
END;
$$ LANGUAGE plpgsql;

SELECT type_testing(0.5);
SELECT type_testing(0.5::float4);
SELECT type_testing(1);

--
CREATE OR REPLACE FUNCTION type_testing2(money_val int) RETURNS void AS $$
BEGIN
	RAISE NOTICE 'ran %', money_val;
END;
$$ LANGUAGE plpgsql;

SELECT type_testing2(1);
SELECT type_testing2(0.5::int); --требуется явное приведение типа - 0.5 преобразуется к 1
SELECT type_testing2(0.3::int); -- 0.3 к 0

SELECT type_testing2(CAST(0.3 AS int)); --другой способ приведения типа

SELECT type_testing2('1.5'::int); --error
SELECT type_testing2('1.5'::numeric::int); --а так работает
SELECT type_testing2('1'::int); --а так работает

SELECT 50! AS big_factorial; --вычисление факториала
SELECT CAST(50 AS bigint)! AS big_factorial; --то как интерпретатор выполняет команду выше

SELECT 'abc' || 1; -- тип text
SELECT ' 10 ' = 10; -- true, стока неявно преобразуется в int, сравниваются 10 и 10 - получаем true

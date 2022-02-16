--массив - коллекция данных одного типа
--нумерация массива начинается с 1

CREATE TABLE chess_game(
	white_player text,
	black_player text,
	moves text[],
	final_state text[][]
);

INSERT INTO chess_game
VALUES
('Caruana', 'Nakamura', 
 ARRAY['d4', 'd5', 'c4', 'e6'],
 ARRAY[['Ra8', 'Qe8', 'x', 'x', 'x', 'x', 'x', 'x'],
	   ['a7',  'x',   'x', 'x', 'x', 'x', 'x', 'x'], 
	   ['Kb5', 'Bc5', 'd5', 'x', 'x', 'x', 'x', 'x']]);

SELECT * FROM chess_game;

SELECT moves[2:3]
FROM chess_game;

SELECT moves[:3] --moves[1:3]
FROM chess_game;

SELECT moves[2:] --от 2 до конца moves
FROM chess_game;

SELECT array_dims(moves), array_dims(final_state), array_length(moves, 1)
FROM chess_game;
--array_dims показывает размерность массива -1:4, 1 одномерный состоящий из 4 элементов
--array_length(moves, 1) - просим выдать число элементов первого элемента массива
-- array_dims(final_state) -[1:3][1:8] - двумерный массив 3 на 8

-- обновляем весь массив moves
UPDATE chess_game
SET moves = ARRAY['e4', 'd5', 'd4', 'Kf6'];

-- обновление по индексу массива
UPDATE chess_game
SET moves[4] = 'g6';

-- находим записи в которых moves содержит g6
SELECT *
FROM chess_game
WHERE 'g6' = ANY(moves);

--102
SELECT ARRAY[1, 2, 3, 4] = ARRAY[1, 2, 3, 4]; --true, поэлементное сравнение
SELECT ARRAY[4, 2, 3, 1] = ARRAY[1, 2, 3, 4]; --false, поэлементное сравнение, 4 != 1
SELECT ARRAY[1, 2, 4, 3] > ARRAY[1, 2, 3, 4]; --true, поэлементное сравнение, 4 > 3
SELECT ARRAY[1, 2, 3, 4] > ARRAY[1, 2, 5, 4]; --false, поэлементное сравнение, 3 < 5

-- содержатся ли элементы ARRAY[1, 2] в ARRAY[1, 2, 3, 4]
SELECT ARRAY[1, 2, 3, 4] @> ARRAY[1, 2]; --true
SELECT ARRAY[1, 2, 3, 4] @> ARRAY[1, 2, 5]; --false, все элементы ARRAY[1, 2, 5] должны быть в ARRAY[1, 2, 3, 4]

-- содержатся ли элементы ARRAY[1, 2] в ARRAY[1, 2, 3, 4]
SELECT ARRAY[1, 2] <@ ARRAY[1, 2, 3, 4]; --true
SELECT ARRAY[1, 2, 6] <@ ARRAY[1, 2, 3, 4]; --false

--пересечение массивов, если есть пересечение хотя бы по одному элементу получим true
SELECT ARRAY[1, 2, 3, 4] && ARRAY[1, 2]; --true
SELECT ARRAY[1, 2, 3, 4] && ARRAY[5]; --false

SELECT *
FROM chess_game
WHERE moves && ARRAY['d4'];

CREATE OR REPLACE FUNCTION filter_even(VARIADIC numbers int[]) RETURNS SETOF int AS $$
BEGIN
	FOR counter IN 1..array_upper(numbers, 1)
	LOOP
		CONTINUE WHEN counter % 2 != 0;
		RAISE NOTICE '%s', counter;
		RETURN NEXT counter;
	END LOOP;
	RAISE NOTICE 'The END';
END;
$$ LANGUAGE plpgsql;

SELECT * FROM filter_even(1, 2, 3, 4, 5, 6, 7, 8);

--через FOREACH counter IN ARRAY
CREATE OR REPLACE FUNCTION filter_even_2(VARIADIC numbers int[]) RETURNS SETOF int AS $$
DECLARE
	counter int;
BEGIN
	--FOR counter IN 1..array_upper(numbers, 1)
	FOREACH counter IN ARRAY numbers
	LOOP
		CONTINUE WHEN counter % 2 != 0;
		RAISE NOTICE '%s', counter;
		RETURN NEXT counter;
	END LOOP;
	RAISE NOTICE 'The END';
END;
$$ LANGUAGE plpgsql;

SELECT * FROM filter_even_2(1, 2, 3, 4, 5, 6, 7, 8);
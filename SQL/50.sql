-- PRIMARY KEY, UNIQUE NOT NULL

CREATE TABLE chair_2
(
	chair_id serial PRIMARY KEY,
	chair_name varchar,
	dean varchar
);

INSERT INTO chair_2
VALUES
(1, 'name', 'dean');

--INSERT INTO chair_2
--VALUES
--(1, 'name', 'dean'); уже существует записть с chair_id = 1

--INSERT INTO chair_2
--VALUES
--(NULL, 'name', 'dean'); первичный ключ не может быть NULL

SELECT * FROM chair_2;

DROP TABLE chair_2;

CREATE TABLE chair_2
(
	chair_id serial UNIQUE NOT NULL,
	chair_name varchar,
	dean varchar
);
-- UNIQUE не накладивает ограничения на NULL
-- UNIQUE NOT NULL почти эквивалент PRIMARY KEY по возможным значениям,
-- однако UNIQUE NOT NULL можно назначить на любой из стобцов, в отличии от
-- PRIMARY KEY который можно установить лишь на один столбец в таблице

SELECT constraint_name
FROM information_schema.key_column_usage
WHERE table_name = 'chair_2'
	AND table_schema = 'public'
	AND column_name = 'chair_id';
	
-- удаляем ограничения	
ALTER TABLE chair_2
DROP CONSTRAINT chair_2_chair_id_key;

-- добавляем ограничения
ALTER TABLE chair_2
ADD PRIMARY KEY(chair_id);
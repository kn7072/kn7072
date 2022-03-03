--перечисление(enum)

--chess_title справочная таблица
CREATE TABLE chess_title(
	title_id serial PRIMARY KEY,
	title text
);

CREATE TABLE chess_player (
	player_id serial PRIMARY KEY,
	first_name text,
	last_name text,
	title_id int REFERENCES chess_title(title_id)
);

INSERT INTO chess_title(title)
VALUES
('Candidate master'),
('FIDE master'),
('Internation master'),
('Grand master')

SELECT * FROM chess_title;

INSERT INTO chess_player(first_name, last_name, title_id)
VALUES
('a', 'b', 4),
('c', 'd', 4),
('e', 'f', 1);

SELECT *
FROM chess_player
JOIN chess_title USING (title_id);

DROP TABLE chess_title CASCADE;
DROP TABLE chess_player;

--хотим избавиться от справочной таблицы chess_title, заменить ее на перечисление
CREATE TYPE chess_title AS ENUM
('Candidate master', 'FIDE master', 'Internation master');

SELECT enum_range(null::chess_title); --чтобы посмотреть все значения в перечислении

ALTER TYPE chess_title
ADD VALUE 'Grand master' AFTER 'Internation master'; --добавляем новое значение 'Grand master' после 'Internation master'

--создаем таблицу в которой title имеет тип перечисляемое
CREATE TABLE chess_player (
	player_id serial PRIMARY KEY,
	first_name text,
	last_name text,
	title chess_title
);

INSERT INTO chess_player(first_name, last_name, title)
VALUES ('Magnus', 'Carlsen', 'Grand master');

SELECT * FROM chess_player;

INSERT INTO chess_player(first_name, last_name, title)
VALUES ('Magnus', 'Carlsen', '111111111'); -- ОШИБКА
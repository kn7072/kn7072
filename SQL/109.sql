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

INSERT INTO chess_player()
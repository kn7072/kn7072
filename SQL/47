-- DDL
CREATE TABLE student
(
	student_id serial,
	first_name varchar,
	last_name varchar,
	birthday date,
	phone varchar
);

CREATE TABLE cathedra
(
	cathedra_id serial,
	cathedra_name varchar,
	daan varchar
);

ALTER TABLE student
ADD COLUMN middle_name varchar;

ALTER TABLE student
ADD COLUMN rating float;

ALTER TABLE student
ADD COLUMN enrolled date;

-- удалить столбец
ALTER TABLE student
DROP COLUMN middle_name;

ALTER TABLE cathedra
RENAME TO chair;

ALTER TABLE crair
RENAME cathedra_name TO chair_name;

ALTER TABLE crair
RENAME cathedra_id TO chair_id;

-- меняем тип столбцов
ALTER TABLE student
ALTER COLUMN first_name SET DATA TYPE varchar(64);
ALTER TABLE student
ALTER COLUMN last_name SET DATA TYPE varchar(64);
ALTER TABLE student
ALTER COLUMN phone SET DATA TYPE varchar(30);

CREATE TABLE faculty
(
	faculty_id serial,
	fuculty_name varchar
);
ALTER TABLE faculty
RENAME fuculty_name TO faculty_name;

INSERT INTO faculty (faculty_name)
VALUES
('faculty_1'),
('faculty_2'),
('faculty_3');

SELECT * FROM faculty;
TRUNCATE TABLE faculty RESTART IDENTITY; -- Таблица не удаляется, только данные
DROP TABLE faculty; -- удаление таблица
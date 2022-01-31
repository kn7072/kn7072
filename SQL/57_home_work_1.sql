SELECT * FROM exam;
DROP TABLE IF EXISTS exam_new;

CREATE TABLE exam_new
(
	exam_id int GENERATED ALWAYS AS IDENTITY UNIQUE NOT NULL,
	exam_name varchar(256),
	exam_date date
);

-- 2. Удалить ограничение уникальности с поля идентификатора
ALTER TABLE exam_new
DROP CONSTRAINT exam_new_exam_id_key;

-- 3. Добавить ограничение первичного ключа на поле идентификатора
ALTER TABLE exam_new
ADD CONSTRAINT PK_exam_exam_id PRIMARY KEY (exam_id);
-- или
ALTER TABLE exam_new
ADD PRIMARY KEY(exam_id);

ALTER TABLE exam_new
DROP CONSTRAINT exam_id;

--4. Создать таблицу person с полями
DROP TABLE IF EXISTS person_new;
CREATE TABLE person_new
(
	person_id int  NOT NULL, -- PRIMARY KEY
	first_name varchar(64) NOT NULL,
	last_name varchar(64) NOT NULL,
	
	CONSTRAINT pk_person_new_person_id PRIMARY KEY(person_id)
);

-- 5. Создать таблицу паспорта с полями:
DROP TABLE IF EXISTS passport;
CREATE TABLE passport
(
	passport_id int PRIMARY KEY NOT NULL,
	serial_number int NOT NULL,
	registration varchar(32),
	person_id int,
	
	CONSTRAINT FK_passport_person_new FOREIGN KEY (person_id) REFERENCES person_new(person_id)
);

-- 6. Добавить колонку веса в таблицу book (создавали ранее) с ограничением, проверяющим вес (больше 0 но меньше 100)
ALTER TABLE book
ADD COLUMN weight decimal CONSTRAINT CHK_book_wight CHECK (weight > 0 AND weight < 100);

SELECT * FROM book
LIMIT 1;

-- 7. Убедиться в том, что ограничение на вес работает (попробуйте вставить невалидное значение)
INSERT INTO book(title, isbn, publisher_id, weight)
VALUES 
('x', 'y', 2, 2),
('x2', 'y2', 3, 101);

-- 8. Создать таблицу student с полями:
CREATE TABLE student_new
(
	id int GENERATED ALWAYS AS IDENTITY,
	full_name varchar(32),
	course int DEFAULT 1
);

-- 9. Вставить запись в таблицу студентов и убедиться, что ограничение на вставку значения по умолчанию работает
INSERT INTO student_new(full_name)
VALUES
('Bob');

SELECT * FROM student_new;

-- 10. Удалить ограничение "по умолчанию" из таблицы студентов
-- https://postgrespro.ru/docs/postgrespro/14/sql-altertable?lang=en
ALTER TABLE student_new
ALTER COLUMN course DROP DEFAULT;






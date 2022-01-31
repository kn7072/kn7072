DROP TABLE IF EXISTS book;

CREATE TABLE book
(
	book_id int NOT NULL,
	title text NOT NULL,
	isbn varchar(32) NOT NULL,
	publisher_id int NOT NULL,
	
	CONSTRAINT PK_book_book_id PRIMARY KEY(book_id)
);

SELECT * FROM book;

-- создаем объект последовательности(book_book_id_seq) и назначаем его на поле book.book_id
CREATE SEQUENCE IF NOT EXISTS book_book_id_seq
START WITH 1 OWNED BY book.book_id;

-- устанавливаем ограничение на book_id, 
-- по умолчанию назначаем следующее значение последовательности nextval('book_book_id_seq')
ALTER TABLE book
ALTER COLUMN book_id SET DEFAULT nextval('book_book_id_seq');

INSERT INTO book(title, isbn, publisher_id)
VALUES('title', 'isbn', 1);
-------------------------------------------------------
-- новый синтаксис создания serial
DROP TABLE IF EXISTS book;

CREATE TABLE book
(
	book_id int GENERATED ALWAYS AS IDENTITY NOT NULL,
	-- book_id int GENERATED ALWAYS AS IDENTITY(START WITH 10 INCREMENT BY 2) NOT NULL,
	title text NOT NULL,
	isbn varchar(32) NOT NULL,
	publisher_id int NOT NULL,
	
	CONSTRAINT PK_book_book_id PRIMARY KEY(book_id)
);

INSERT INTO book(title, isbn, publisher_id)
VALUES('title', 'isbn', 1);
SELECT * FROM book;

INSERT INTO book
-- OVERRIDING SYSTEM VALUE -- чтобы обойти ошибку ниже
VALUES(5, 'title', 'isbn', 1); -- ошибка, запрещено явно указывать значиние полю book_id(ALWAYS запрещает указывать значение явно)

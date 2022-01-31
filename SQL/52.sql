-- CHECK

DROP TABLE IF EXISTS book;

CREATE TABLE book
(
	book_id int,
	title text NOT NULL,
	isbn varchar(32) NOT NULL,
	publisher_id int,
	
	CONSTRAINT PK_book_book_id PRIMARY KEY(book_id)
);

ALTER TABLE book
ADD COLUMN price decimal CONSTRAINT CHK_book_price CHECK (price >= 0);

INSERT INTO book
VALUES
(1, '1', '11', 1, 1),
(2, '2', '11', 1, 2),
(3, '3', '11', 1, 3);

SELECT * FROM book;

INSERT INTO book
VALUES
(4, '1', '11', 1, -2);


SELECT * FROM book;

INSERT INTO book(title, isbn, publisher_id)
VALUES 
('x1', 'x1', 11),
('x2', 'x2', 12),
('x3', 'x3', 13);

SELECT *
INTO best_book -- создаем таблицу best_book из таблицы book
FROM book
WHERE title IN ('x1', 'x2');

SELECT * FROM best_book;

-- заполняем таблицу best_book результатом select из таблицы book
INSERT INTO best_book
SELECT *
FROM book
WHERE isbn = 'x3'
RETURNING book_id 
-- RETURNING чтобы получить поля получаемые во время запроса
-- RETURNING book_id -получаем значения book_id
-- RETURNING * -получить значения всех полей
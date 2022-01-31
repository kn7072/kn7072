SELECT * FROM book;

-- обновляем запись таблицы
UPDATE book
SET title = 'x4', publisher_id = 100
WHERE book_id = 5;

-- удалить запись в таблице
DELETE FROM book
WHERE title = 'title'
RETURNING * ;

-- удалить все записи в таблице
DELETE FROM book;

-- удалить все записи в таблице, логи не пишит, работает быстрее
TRUNCATE TABLE book;
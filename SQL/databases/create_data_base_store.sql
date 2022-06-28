-- - Магазин. в Нем id и адрес
-- - Товары.  В нем ид товара, название
-- - Продажи. Дата, Сумма, ИдМагазина, ИдТовара
-- Нужно вывести адрес магазина, в котором было максимальное число продаж определенного товара (бананов) за определенную дату (за сегодня)
CREATE DATABASE store;

DROP TABLE IF EXISTS store;

\c store

CREATE TABLE store (
    store_id int GENERATED ALWAYS AS IDENTITY NOT NULL,
    address varchar NOT NULL,

    CONSTRAINT pk_store_store_id PRIMARY KEY(store_id)

);

INSERT INTO store(address)
VALUES 
('a'),
('b'),
('c'),
('d'),
('f');

DROP TABLE IF EXISTS goods;

CREATE TABLE goods (
    good_id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY NOT NULL,
    good_name varchar NOT NULL
);

INSERT INTO goods(good_name)
VALUES
('milk'),
('bread'),
('butter'),
('banana'),
('cherry'),
('vine');

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    date_sale date,
    good_id int,
    store_id int,
    sum int NOT NULL,

    CONSTRAINT fk_sales_store_id FOREIGN KEY (store_id) REFERENCES store(store_id),
    CONSTRAINT fk_sales_good_id FOREIGN KEY (good_id) REFERENCES goods(good_id)
);

INSERT INTO sales
VALUES
('2022-06-28', 1, 1, 1),
('2022-06-27', 2, 1, 1),
('2022-06-25', 3, 2, 1),
('2022-06-24', 4, 2, 1),
('2022-06-28', 5, 3, 1),
('2022-05-28', 1, 1, 1),
('2022-05-27', 2, 2, 2),
('2022-05-27', 2, 1, 1),
('2022-05-27', 2, 1, 1),
('2022-05-27', 2, 3, 1),
('2022-05-27', 2, 3, 2),
('2022-05-27', 2, 1, 1),
('2022-05-25', 3, 2, 1),
('2022-05-24', 4, 2, 1),
('2022-05-28', 5, 3, 1),
('2022-05-25', 3, 4, 1),
('2022-05-24', 4, 4, 1),
('2022-05-28', 5, 5, 1);

WITH sum_goods AS (
    SELECT store_id, SUM(sum) as total_sum
    FROM sales s JOIN goods g ON s.good_id = g.good_id
    WHERE date_sale = '2022-05-27' AND good_name = 'bread'
    GROUP BY store_id)
SELECT address, total_sum FROM store, sum_goods
WHERE store.store_id = sum_goods.store_id AND total_sum = (SELECT MAX(total_sum) FROM sum_goods);


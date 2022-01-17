SELECT MAX(product_id) FROM products;

-- 11. Подключиться к БД northwind и добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products
ADD CONSTRAINT CHK_products_unit_price CHECK (unit_price > 0);

CREATE SEQUENCE products_product_id
START WITH 78 OWNED BY products.product_id;

-- 12. "Навесить" автоинкрементируемый счётчик на поле product_id таблицы products (БД northwind). Счётчик должен начинаться с числа следующего за максимальным значением по этому столбцу.
ALTER TABLE products
ALTER COLUMN product_id SET DEFAULT nextval('products_product_id');


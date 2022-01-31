SELECT company_name, contact_name
FROM customers
-- WHERE EXISTS возвращает true если находится хотя бы одна запись
WHERE EXISTS (SELECT customer_id FROM orders
			 WHERE customer_id = customers.customer_id
			 AND freight BETWEEN 50 AND 100);
			 
SELECT company_name, contact_name
FROM customers
-- заказчики которые не делали заказы в интервале '1995-02-01'- '1995-02-15'
WHERE NOT EXISTS (SELECT customer_id FROM orders
			 WHERE customer_id = customers.customer_id
			 AND order_date BETWEEN '1995-02-01' AND '1995-02-15');
			 
-- выбрать продукты которые не покупались в интервале '1995-02-01'- '1995-02-15'
SELECT product_name
FROM products
WHERE NOT EXISTS (SELECT orders.order_id FROM orders
				 JOIN order_details USING(order_id)
				 WHERE order_details.product_id = product_id
				 AND order_date BETWEEN '1995-02-01' AND '1995-02-15');

-- находим уникальные компании которые купили более 40 единиц товара
SELECT DISTINCT company_name
FROM customers
JOIN orders USING(customer_id)
JOIN order_details USING(order_id)
WHERE quantity > 40;
-- или 
SELECT DISTINCT company_name
FROM customers
WHERE customer_id = ANY( -- хотябы одно совпадение
	SELECT customer_id
	FROM orders
	JOIN order_details USING(order_id)
	WHERE quantity > 40	
);

SELECT DISTINCT product_name, quantity
FROM products
JOIN order_details USING(product_id)
WHERE quantity > (
	SELECT AVG(quantity)
	FROM order_details
)
ORDER BY quantity;

---

-- найти продукты, количество которых больше чем любого(ALL всех) среднего
SELECT DISTINCT product_name
FROM products
JOIN order_details USING(product_id)
WHERE quantity > ALL(SELECT AVG(quantity)
					FROM order_details
					GROUP BY product_id);


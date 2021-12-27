--1
SELECT product_name, units_in_stock
FROM products
WHERE units_in_stock < ALL(
SELECT AVG(quantity) 
FROM order_details
GROUP BY product_id)
ORDER BY units_in_stock DESC;

--2
SELECT customer_id, SUM(freight) AS freight_sum
FROM orders
INNER JOIN (SELECT customer_id, AVG(freight) AS freight_avg
				  FROM orders
				  GROUP BY customer_id) ao
USING(customer_id)				  
WHERE freight > freight_avg AND shipped_date BETWEEN '1996-07-16' AND '1996-07-31'
GROUP BY customer_id
ORDER BY freight_sum;

--3
SELECT customer_id, ship_country, order_price
FROM orders
JOIN (SELECT order_id, SUM(unit_price * quantity - unit_price * quantity * discount) AS order_price
		FROM order_details
		GROUP BY order_id) AS od
USING(order_id)		
WHERE order_date >= '1997-09-01' AND ship_country IN ('Chile', 'Brazil', 'Peru', 'Venezuela')
ORDER BY order_price DESC
LIMIT 3;

--4
SELECT DISTINCT product_name
FROM products
WHERE product_id = ANY(
				SELECT product_id 
				FROM order_details
				WHERE quantity = 10
);
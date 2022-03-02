SELECT company_name
FROM suppliers
WHERE country IN (SELECT country FROM customers);

--CTE временная таблица
WITH customer_countries AS
(
	SELECT country FROM customers
)

SELECT company_name
FROM suppliers
WHERE country IN (SELECT * FROM customer_countries);

SELECT company_name
FROM suppliers
WHERE NOT EXISTS 
	(
		SELECT product_id
		FROM products
		JOIN order_details USING(product_id)
		JOIN orders USING(order_id)
		WHERE suppliers.supplier_id = products.supplier_id AND
			order_date BETWEEN '1998-02-01' AND '1998-02-04'
	);
	
	
	
	
	
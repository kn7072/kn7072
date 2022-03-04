SELECT *
FROM products
WHERE product_id = ANY (
	SELECT product_id
	FROM (
		SELECT product_id, unit_price,
				ROW_NUMBER() OVER(ORDER BY unit_price DESC) AS nth
		FROM products
	) sorted_prices
	WHERE nth < 4
);

--или тоже самое, но с меньшей вложенностью
SELECT *
FROM (SELECT product_id, product_name, category_id, unit_price, units_in_stock,
				ROW_NUMBER() OVER(ORDER BY unit_price DESC) AS nth
		FROM products) AS sorted_prices
WHERE nth < 4
ORDER BY unit_price;

SELECT *
FROM
(
	SELECT order_id, product_id, unit_price, quantity,
			RANK() OVER(PARTITION BY order_id ORDER BY quantity DESC) AS rank_quant
	FROM orders
	JOIN order_details USING(order_id)
) AS subquery
WHERE rank_quant <= 3;



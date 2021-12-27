SELECT company_name
FROM suppliers
WHERE country IN (SELECT DISTINCT country
                  FROM customers);

SELECT DISTINCT suppliers.company_name
FROM suppliers
JOIN customers USING(country);

--
SELECT category_name, SUM(units_in_stock) AS sum_unints
FROM products
INNER JOIN categories USING(category_id)
GROUP BY category_name
ORDER BY sum_unints DESC
LIMIT (SELECT MIN(product_id) + 4 FROM products);

SELECT product_name, units_in_stock
FROM products
WHERE units_in_stock > (SELECT AVG(units_in_stock) FROM products)
ORDER BY units_in_stock;
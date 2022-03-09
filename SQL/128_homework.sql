SELECT DISTINCT orders.employee_id
FROM orders;

--Вывести отчёт показывающий по сотрудникам суммы продаж SUM(unit_price*quantity), 
--и сопоставляющий их со средним значением суммы продаж по сотрудникам (AVG по SUM(unit_price*quantity))
--сортированный по сумме продаж по убыванию.
SELECT employee_id, order_total_price, 
					AVG(order_total_price) OVER()
FROM (
	SELECT employee_id, SUM(unit_price * quantity) AS order_total_price
	FROM order_details
	JOIN orders USING(order_id)
	GROUP BY employee_id
) AS sub_query
ORDER BY order_total_price DESC;

--Вывести ранг сотрудников по их зарплате, без пропусков. 
--Также вывести имя, фамилию и должность.
SELECT DENSE_RANK() OVER(ORDER BY salary DESC) salary_rank, salary, 
		first_name, last_name, title
FROM employees;		

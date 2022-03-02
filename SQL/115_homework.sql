--Вывести сумму продаж (цена * кол-во) по каждому сотруднику с подсчётом полного итога (полной суммы по всем сотрудникам) отсортировав по сумме продаж (по убыванию).
SELECT employee_id, SUM(quantity * unit_price) AS total_summary FROM orders
JOIN order_details AS od USING(order_id)
GROUP BY ROLLUP (employee_id)
ORDER BY total_summary DESC NULLS FIRST;

--Вывести отчёт показывающий сумму продаж по сотрудникам и странам отгрузки с подытогами по сотрудникам и общим итогом.
SELECT employee_id, ship_country, SUM(quantity * unit_price) AS total_summary 
FROM orders
JOIN order_details AS od USING(order_id)
--JOIN employees AS emp USING(emloyee_id)
GROUP BY ROLLUP (employee_id, ship_country)
ORDER BY employee_id, total_summary DESC NULLS FIRST;

--Вывести отчёт показывающий сумму продаж по сотрудникам, странам отгрузки, сотрудникам и странам отгрузки с подытогами по сотрудникам и общим итогом.
SELECT employee_id, ship_country, SUM(quantity * unit_price) AS total_summary 
FROM orders
JOIN order_details AS od USING(order_id)
GROUP BY CUBE (employee_id, ship_country)
ORDER BY employee_id, total_summary DESC NULLS FIRST;


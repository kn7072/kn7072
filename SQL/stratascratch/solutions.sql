-- https://platform.stratascratch.com/coding/10350-algorithm-performance?code_type=1
-- Algorithm Performance

SELECT search_id, max_rating
FROM (
    SELECT search_id, MAX(CASE WHEN clicked = 0 THEN 1
                          WHEN clicked > 0 AND search_results_position > 3 THEN 2
                          WHEN clicked > 0 AND search_results_position <= 3 THEN 3
                          END) max_rating
    FROM fb_search_events
    GROUP BY search_id
) sub
ORDER BY search_id;

-- https://platform.stratascratch.com/coding/10324-distances-traveled?code_type=1
-- Distances Traveled
SELECT user_id, name, sum_distance
FROM (
    SELECT user_id, name, sum_distance, (DENSE_RANK() OVER (ORDER BY sum_distance DESC)) dr --FILTER (WHERE dr <= 10)
    FROM (
        SELECT user_id, name, SUM(distance) sum_distance
        FROM lyft_rides_log lr
        JOIN lyft_users lu ON lu.id = lr.user_id
        GROUP BY user_id, name
        ORDER BY SUM(distance) DESC
    ) sub
) sub2
WHERE dr <= 10;

SELECT user_id, name, sum_distance
FROM (
        SELECT user_id, name, SUM(distance) sum_distance
        FROM lyft_rides_log lr
        JOIN lyft_users lu ON lu.id = lr.user_id
        GROUP BY user_id, name
        ORDER BY SUM(distance) DESC
) sub
LIMIT 10;

-- https://platform.stratascratch.com/coding/10318-new-products?code_type=1
-- New Products
SELECT company_name, y_20 - y_19 diff
FROM (
    SELECT company_name, COUNT(*) FILTER ( WHERE year = 2019) y_19, 
                         COUNT(*) FILTER ( WHERE year = 2020) y_20
    FROM car_launches
    GROUP BY company_name
) sub;

-- https://platform.stratascratch.com/coding/10315-cities-with-the-most-expensive-homes?code_type=1
-- Cities With The Most Expensive Homes
WITH average AS (
    SELECT city, AVG(mkt_price) avg_price
    FROM zillow_transactions
    GROUP BY city
)
SELECT city
FROM average
WHERE avg_price > (SELECT AVG(mkt_price) FROM zillow_transactions);

SELECT city
from zillow_transactions
GROUP BY city
HAVING avg(mkt_price) > (select avg(mkt_price) from zillow_transactions)


-- https://platform.stratascratch.com/coding/10310-class-performance?code_type=1
-- Class Performance

WITH sub AS (
    SELECT student, (assignment1 + assignment2 + assignment3) s
    FROM box_scores
)
SELECT MAX(s) - MIN(s)
FROM sub;

-- https://platform.stratascratch.com/coding/10304-risky-projects?code_type=1
-- Risky Projects

WITH sub AS (
    SELECT lp.title, lp.budget, ceil((lp.end_date - lp.start_date)/365::float * SUM(le.salary)) sum_salary
    FROM linkedin_projects lp
    JOIN linkedin_emp_projects lep ON lp.id = lep.project_id
    JOIN linkedin_employees le ON lep.emp_id = le.id
    GROUP BY lp.title, lp.budget, (lp.end_date - lp.start_date)
)
SELECT title, budget, sum_salary
FROM sub
WHERE sum_salary > budget;

-- https://platform.stratascratch.com/coding/10301-expensive-projects?code_type=1
-- Expensive Projects
SELECT title, ceil(budget/COUNT(*)::float)
FROM ms_projects msp
JOIN ms_emp_projects mse ON msp.id = mse.project_id
GROUP BY title, budget
ORDER BY ceil(budget/COUNT(*)::float) DESC;

-- https://platform.stratascratch.com/coding/10295-most-active-users-on-messenger?code_type=1
-- Most Active Users On Messenger
WITH Parent AS (
SELECT sub.user usr, sub.s su, DENSE_RANK() OVER(ORDER BY sub.s DESC) dr
FROM (SELECT user1 AS user, SUM(msg_count) AS s
FROM fb_messages
GROUP BY user1
UNION 
SELECT user2 AS user, SUM(msg_count) AS s
FROM fb_messages
GROUP BY user2) sub
)
SELECT usr, su
FROM Parent
WHERE dr <= 10;


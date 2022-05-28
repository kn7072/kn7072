SELECT *
FROM emp
ORDER BY CASE WHEN job = 'SALESMAN' THEN comm
              ELSE sal
END;  


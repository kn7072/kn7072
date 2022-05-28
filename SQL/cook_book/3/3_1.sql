SELECT ename, deptno 
FROM emp
UNION ALL
SELECT '--------', NULL
UNION ALL
SELECT job, deptno
FROM emp;

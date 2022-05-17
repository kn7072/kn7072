--2.1 Returning Query Results in a Specified Order
select ename,job,sal
from emp
where deptno = 10
order by sal asc;

# 2.3 Sorting by Substrings
select ename,job
from emp
order by substr(job,length(job)-1);

--2.1 Returning Query Results in a Specified Order
SELECT ename, job, sal
FROM emp
WHERE deptno = 10
ORDER BY sal ASC;

--2.2 Sorting by Multiple Fields
SELECT empno, deptno, sal, ename, job
FROM emp
ORDER BY deptno, sal DESC;

--2.3 Sorting by Substrings
SELECT ename, job
FROM emp
ORDER BY substr(job, length(job) - 1);

--2.4 Sorting Mixed Alphanumeric Data
CREATE VIEW V AS
SELECT ename || ' ' || deptno AS data
FROM emp;

SELECT * FROM V;

SELECT data
FROM V
ORDER BY replace(translate(data, '0123456789', '##########'), '#', '');

SELECT translate('abcdefg', 'bca', ''); --BCA

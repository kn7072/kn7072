select * from emp
where deptno = 10;

select *
from emp
where deptno = 10 
	or comm is not NULL
	or sal <= 2000 and deptno = 20;

--1.3 Finding Rows That Satisfy Multiple Conditions
select *
from emp
where (
		deptno = 10
		or comm is not null
		or sal <= 2000
	) and deptno = 20;

--1.6 Referencing an Aliased Column in the WHERE Clause
-- select sal as salary, comm as commission
-- from emp
-- where salary < 5000

select *
from (
		select sal as salary, comm as commission
		from emp
 	) x
where salary < 5000;

--1.7 Concatenating Column Values
select ename || ' WORKS AS A ' || job as msg
from emp
where deptno=10;

--1.8 Using Conditional Logic in a SELECT Statement
select ename, sal,
			case when sal <= 2000 then 'UNDERPAID'
				 when sal >= 4000 then 'OVERPAID'
                 else 'OK'
            end as status
from emp;

--1.9 Limiting the Number of Rows Returned
select *
from emp 
limit 5;

--1.10 Returning n Random Records from a Table
select ename, job
from emp
order by random()
limit 5;

--1.11 Finding Null Values
select *
from emp
where comm is null;

--1.12 Transforming Nulls into Real Values
select coalesce(comm, 0)
from emp;

--1.13 Searching for Patterns
select ename, job
from emp
where deptno in (10, 20) and (ename like '%I%' or ename like '%ER');

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

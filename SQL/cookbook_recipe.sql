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


# 2.3 Sorting by Substrings
select ename,job
from emp
order by substr(job,length(job)-1);


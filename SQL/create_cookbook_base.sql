SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE DATABASE sql_cookbook
    WITH 
    OWNER = 'che'
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

DROP TABLE IF EXISTS EMP;
------------------------------------------
CREATE TABLE EMP(
	EMPNO int,
	ENAME varchar,
	JOB varchar,
	MGR int,
	HIREDATE date,
	SAL int,
	COMM int,
	DEPTNO int
);

INSERT INTO EMP
VALUES
(7369, 'SMITH',  'CLERK',      7902, '17-DEC-2005', 800,  NULL, 20),
(7499, 'ALLEN',  'SALESMAN',   7698, '20-FEB-2006', 1600, 300,  30),
(7521, 'WARD',   'SALESMAN',   7698, '22-FEB-2006', 1250, 500,  30),
(7566, 'JONES',  'MANAGER',    7839, '02-APR-2006', 2975, NULL, 20),
(7654, 'MARTIN', 'SALESMAN',   7698, '28-SEP-2006', 1250, 1400, 30),
(7698, 'BLAKE',  'MANAGER',    7839, '01-MAY-2006', 2850, NULL, 30),
(7782, 'CLARK',  'MANAGER',    7839, '09-JUN-2006', 2450, NULL, 10),
(7788, 'SCOTT',  'ANALYST',    7566, '09-DEC-2007', 3000, NULL, 20),
(7839, 'KING',   'PRESIDENT',  NULL, '17-NOV-2006', 5000, NULL, 10),
(7844, 'TURNER', 'SALESMAN',   7698, '08-SEP-2006', 1500, 0,    30),
(7876, 'ADAMS',  'CLERK',      7788, '12-JAN-2008', 1100, NULL, 20),
(7900, 'JAMES',  'CLERK',      7698, '03-DEC-2006', 950,  NULL, 30),
(7902, 'FORD',   'ANALYST',    7566, '03-DEC-2006', 3000, NULL, 20),
(7934, 'MILLER', 'CLERK',      7782, '23-JAN-2007', 1300, NULL, 10)

select * from emp;
------------------------------------------
DROP TABLE IF EXISTS DEPT;
CREATE TABLE DEPT(
	DEPTNO int,
	DNAME varchar,
	LOC varchar
);

INSERT INTO DEPT
VALUES
(10, 'ACCOUNTING', 'NEW YORK'),
(20, 'RESEARCH',   'DALLAS'),
(30, 'SALES',      'CHICAGO'),
(40, 'OPERATIONS', 'BOSTON')

select * from dept;
------------------------------------------
DROP TABLE IF EXISTS T1;
CREATE TABLE T1(
	ID int
);

INSERT INTO T1
VALUES
(1);

select id from t1;
------------------------------------------
DROP TABLE IF EXISTS T10;
CREATE TABLE T10(
	ID int
);

INSERT INTO T10
VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10);

select id from t10;
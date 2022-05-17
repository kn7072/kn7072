--DROP VIEW  IF EXISTS v;

--CREATE VIEW v AS
--SELECT replace(mixed,' ','') AS mixed
--FROM
-- (
--        SELECT
--                substr(ename,1,2)||
--                cast(deptno AS char(4))||
--                substr(ename,3,2) AS mixed
--        FROM emp WHERE deptno = 10
--        UNION ALL
--        SELECT
--                cast(empno as char(4)) AS mixed
--        FROM emp
--        WHERE deptno = 20
--        UNION ALL
--        SELECT
--                ename as mixed
--        FROM emp
--        WHERE deptno = 30
--) x;

--SELECT * from v;

--SELECT '---------------------------';

SELECT only_digits
FROM (
        SELECT REGEXP_REPLACE(mixed, '[^\d]', '', 'g') AS only_digits
        FROM v

) x
WHERE length(only_digits) > 0;

--SELECT '----------------------------';
SELECT REGEXP_REPLACE('7CL10A+R', '[^\d]', '', 'g');

--SELECT SUBSTRING('XY1234Z', 'Y*([0-9]{1,3})');

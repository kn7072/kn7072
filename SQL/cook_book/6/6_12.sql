--DROP VIEW IF EXISTS v;
SELECT *
FROM emp;

--SELECT version();

SELECT string_agg(ch, '')
FROM (
        SELECT (string_to_table(ename, NULL)) as ch, ctid --empno
        FROM emp
        ORDER BY ch
) y
GROUP BY ctid ; --empno

--DROP VIEW IF EXISTS v;
--
--CREATE VIEW v AS
--SELECT 'mo,larry,curly' AS name
--FROM t1
--UNION ALL
--SELECT 'tina,gina,jaunita,regina,leena' AS name
--FROM t1
--UNION ALL
--SELECT '' AS name
--FROM t1
--UNION ALL
--SELECT 'x, ,z' AS name
--FROM t1;


--SELECT *
--FROM v;
--
--SELECT replace(substring('tina,gina,jaunita,regina,leena' FROM ',\w+'), ',', '');
--SELECT replace(substring('' FROM ',\w+'), ',', '');
------------------------------------------
--
SELECT two_word
FROM (
        SELECT replace(substring(name FROM ',[\w\s]+'), ',', '') as two_word
        FROM v
) x
WHERE length(two_word) > 0;
--
----------------------------------------
--SELECT two_word
--FROM (
--        SELECT (string_to_array(name, ','))[2] as two_word
--        FROM v
--) x
--WHERE length(two_word) > 0;

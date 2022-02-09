CREATE OR REPLACE FUNCTION get_season(month_number int) RETURNS text AS $$
DECLARE
	season text;
BEGIN
    IF month_number NOT BETWEEN 1 AND 12 THEN
		RAISE EXCEPTION 'Invalid month. You passed: (%)', month_number USING HINT='Allowed from 1 up 12', ERRCODE=12882;
	END IF;	
	
	IF month_number BETWEEN 3 AND 5 THEN
		season = 'Spring';
	ELSEIF month_number BETWEEN 6 AND 8 THEN
		season = 'Summer';
	ELSEIF month_number BETWEEN 9 AND 11 THEN
		season = 'Autum';	
	ELSE
		season = 'Winter';
	END IF;
	
	RETURN season;
END;
$$ LANGUAGE plpgsql;

SELECT get_season(15);

CREATE OR REPLACE FUNCTION get_season_caller(month_number int) RETURNS text AS $$
DECLARE
	err_ctx text;
	err_msg text;
	err_details text;
	err_code text;
BEGIN
	RETURN get_season(month_number);
EXCEPTION WHEN SQLSTATE '12882' THEN
	GET STACKED DIAGNOSTICS
		err_ctx = PG_EXCEPTION_CONTEXT,
		err_msg = MESSAGE_TEXT,
		err_details = PG_EXCEPTION_DETAIL,
		err_code = RETURNED_SQLSTATE;
	RAISE INFO 'My custom handler.';
	RAISE INFO 'Error msg:%', err_msg;
	RAISE INFO 'Error details:%', err_details;
	RAISE INFO 'Error code:%', err_code;
	RAISE INFO 'Error context:%', err_ctx;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

SELECT get_season_caller(15);


CREATE OR REPLACE FUNCTION get_season_caller_2(month_number int) RETURNS text AS $$
BEGIN
	RETURN get_season(month_number);
EXCEPTION 
WHEN SQLSTATE '12000' THEN
	RAISE INFO 'My custom handler.';
	RAISE INFO 'Error name:%', SQLERRM; --еще один способ узнать об ошибке, не использую GET STACKED DIAGNOSTICS
	RAISE INFO 'Error details:%', SQLSTATE;
	RETURN NULL;
WHEN OTHERS THEN
	--если ошибке не была перехвачена условиями выше
	RAISE INFO 'Ошибка с неизвестным кодом.';
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

SELECT get_season_caller_2(15);
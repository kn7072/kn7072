--drop function if exists should_increase_salary;

create or replace function should_increase_salary(
	cur_salary numeric,
	max_salary numeric DEFAULT 80, 
	min_salary numeric DEFAULT 30,
	increase_rate numeric DEFAULT 0.2
	) returns bool AS $$
declare
	new_salary numeric;
	err_msg_1 text;
	err_msg_2 text;
	err_msg_3 text;
begin
	
	if min_salary > max_salary then
		err_msg_1 = format('Максимальная зарплата %s меньше минимальной %s', max_salary, min_salary);
		raise exception '%', err_msg_1 using hint='x', errcode='12345';
	end if;
	
	if min_salary < 0 OR max_salary < 0 then
		err_msg_2 = format('Одно(или оба) значиний меньше 0, max_salary %s min_salary %s', max_salary, min_salary);
		raise exception '%', err_msg_2 using hint='y', errcode='12346';
	end if;
	
	if increase_rate < 0.05 then
	    err_msg_3 = format('Коэфициент повышения не может быть меньше %s', increase_rate);
		raise info 'Коэфициент повышения не может быть меньше %', increase_rate;
		raise exception '%', err_msg_3 using hint='z', errcode='12347';
	end if;
	
	if cur_salary >= max_salary or cur_salary >= min_salary then 		
		return false;
	end if;
	
	if cur_salary < min_salary then
		new_salary = cur_salary + (cur_salary * increase_rate);
	end if;
	
	if new_salary > max_salary then
		return false;
	else
		return true;
	end if;	
end;
$$ language plpgsql;

SELECT should_increase_salary(79, 10, 80, 0.2);
SELECT should_increase_salary(79, 10, -1, 0.2);
SELECT should_increase_salary(79, 10, 10, 0.04);

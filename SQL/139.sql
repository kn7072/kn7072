--список ролей
--postgres имеет привилегии супер пользователя
SELECT rolname FROM pg_roles;

DROP ROLE IF EXISTS northwind_admins;

--создаем роли, пока пустые роли - при помощи их нельзя подключиться к базе
CREATE ROLE sales_stuff;
CREATE ROLE northwind_admins;

-- удаляем пользователей(роли)
DROP USER join_smith;
DROP USER north_admin1;

-- создаем пользователей(роли)
CREATE USER join_smith WITH PASSWORD '123';
CREATE USER north_admin1 WITH PASSWORD '123';
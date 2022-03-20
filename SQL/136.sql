--аудит таблиц
DROP TABLE IF EXISTS products_audit;

CREATE TABLE products_audit
(
	op char(1) NOT NULL,
	user_changed text NOT NULL,
	time_stamp timestamp NOT NULL,
	
	product_id smallint NOT NULL,
	product_name varchar(40) NOT NULL,
	supplier_id smallint,
	category_id smallint,
	quantity_per_unit varchar(20),
	unit_price real,
	unit_in_stock smallint,
	unit_on_order smallint,
	reorder_level smallint,
	discontinued integer NOT NULL
);

CREATE OR REPLACE FUNCTION build_audit_products() RETURNS trigger AS $$
BEGIN
	IF TG_OP = 'INSERT' THEN
		INSERT INTO products_audit
		SELECT 'I', session_user, now(), nt.* FROM new_table nt;
	ELSEIF TG_OP = 'UPDATE' THEN
		INSERT INTO products_audit
		SELECT 'U', session_user, now(), nt.* FROM new_table nt;
	ELSEIF TG_OP = 'DELETE' THEN
		INSERT INTO products_audit
		SELECT 'D', session_user, now(), ot.* FROM old_table ot;
	END IF;
	RETURN NULL; --авто тригер, NULL не отменяет авто тригер
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_products_insert ON products;
CREATE TRIGGER audit_products_insert AFTER INSERT ON products
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE PROCEDURE build_audit_products();

DROP TRIGGER IF EXISTS audit_products_update ON products;
CREATE TRIGGER audit_products_update AFTER UPDATE ON products
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT EXECUTE PROCEDURE build_audit_products();

DROP TRIGGER IF EXISTS audit_products_delete ON products;
CREATE TRIGGER audit_products_delete AFTER DELETE ON products
REFERENCING OLD TABLE AS old_table
FOR EACH STATEMENT EXECUTE PROCEDURE build_audit_products();

SELECT * FROM products ORDER BY product_id DESC;

INSERT INTO products
VALUES (79, 'xxx', 7, 4, 'xxx', 50, 20, 0, 0, 0);

--проверяем результат
SELECT * FROM products_audit;

UPDATE products
SET unit_price = 100
WHERE product_id = 79;

DELETE FROM products
WHERE product_id = 79;

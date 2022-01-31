CREATE TABLE publisher
(
	publisher_id integer PRIMARY KEY,
	org_name varchar(120) NOT NULL,
	address text NOT NULL
);

CREATE TABLE book
(
	book_id integer PRIMARY KEY,
	title text NOT NULL,
	isbn varchar(32) NOT NULL,
	fk_publisher_id integer REFERENCES publisher(publisher_id)
);

CREATE TABLE person
(
	person_id int PRIMARY KEY,
	first_name varchar(64) NOT NULL,
	last_name varchar(64) NOT NULL
);

CREATE TABLE passport
(
	passport_id int PRIMARY KEY,
	serial_number int NOT NULL,
	fk_passport_person int REFRENCES person(person_id)
);

ALTER TABLE passport
ADD COLUMN registration text NOT NULL

-- DROP TABLE IF EXISTS book;
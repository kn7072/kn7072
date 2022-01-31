-- многие ко многим
CREATE TABLE book
(
	book_id int PRIMARY KEY,
	title text NOT NULL,
	isbn text NOT NULL
);

CREATE TABLE author
(
	author_id int PRIMARY KEY,
	full_name text NOT NULL,
	rating real
);

CREATE TABLE book_author
(
	book_id int REFERENCES book(book_id),
	author_if int REFERENCES author(author_id),
	CONSTRAINT book_author_pkey PRIMARY KEY (book_id, author_id) -- composite key
)

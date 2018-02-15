CREATE TABLE IF NOT EXISTS journal(
	id integer PRIMARY KEY,
	log_date text NOT NULL,
	count integer NOT NULL
);
----

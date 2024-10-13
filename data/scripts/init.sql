create schema test_db;

CREATE TABLE test_db."user"
(
    id SERIAL NOT NULL,
    username varchar (20) NOT NULL,
    password varchar (100) NOT NULL,
    token varchar (100) NOT NULL,
    token_activate_at timestamp without time zone NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'utc'::text)
);

CREATE TABLE test_db."product"
(
    id SERIAL NOT NULL,
    name varchar (20) NOT NULL,
    unit_price real NOT NULL,
    quantity integer NOT NULL DEFAULT 0
);
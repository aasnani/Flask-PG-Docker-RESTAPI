-- Unused .sql file to initialize DB previously

CREATE USER flaskapp NOSUPERUSER PASSWORD 'flaskapp';

CREATE TABLE IF NOT EXISTS Authors(
    id integer primary key generated always as identity,
    name text,
    bio text,
    birth_date date
);

CREATE TABLE IF NOT EXISTS Books(
    id integer primary key generated always as identity,
    title text,
    description text,
    publish_date date,
    author_id integer references Authors(id) ON DELETE CASCADE
);
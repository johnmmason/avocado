-- schema.sql

\c avocado;

CREATE TABLE avocado(
    id SERIAL PRIMARY KEY,
    week_id INTEGER,
    week DATE,
    price REAL,
    volume REAL,
    total_4046 REAL,
    total_4225 REAL,
    total_4770 REAL,
    category VARCHAR(20),
    year INTEGER,
    region VARCHAR(20)
);

COPY avocado(week_id, week, price, volume, total_4046, total_4225, total_4770, category, year, region)
FROM '/avocado.csv'
DELIMITER ','
CSV HEADER;

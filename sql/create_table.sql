-- DDL Blueprint untuk tabel users_etl di PostgreSQL
CREATE TABLE IF NOT EXISTS users_etl (
    id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    gender VARCHAR(15),
    email VARCHAR(100),
    phone VARCHAR(50),
    username VARCHAR(50),
    birth_date DATE,
    blood_group VARCHAR(5),
    height NUMERIC,
    weight NUMERIC,
    university VARCHAR(150),
    role VARCHAR(30)
);
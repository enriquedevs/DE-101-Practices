USE Fundamentals_DB;
USE WAREHOUSE COMPUTE_WH;

CREATE TABLE products (
  name varchar(500),
  description varchar(500),
  price FLOAT,
  stock FLOAT,
  valid_for_year INTEGER
)
--create a database for tests
DROP DATABASE IF EXISTS test_db;
CREATE DATABASE test_db;
\c test_db
CREATE EXTENSION IF NOT EXISTS postgis;

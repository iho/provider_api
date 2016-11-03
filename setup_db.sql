CREATE USER api_test_user WITH ENCRYPTED PASSWORD 'password' CREATEDB;
CREATE DATABASE  api_test_db WITH ENCODING 'UTF-8' OWNER "api_test_user";
GRANT ALL PRIVILEGES ON DATABASE api_test_db TO api_test_user;

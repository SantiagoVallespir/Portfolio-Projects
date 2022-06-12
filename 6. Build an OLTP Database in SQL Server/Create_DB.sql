-- Create the DB
CREATE DATABASE RetailShopProject;

USE RetailShopProject;

-- Create tables
CREATE TABLE order_details(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	customer_id INTEGER NOT NULL,
	total_price FLOAT NOT NULL,
	payment_status BIT NOT NULL,
	created_at DATETIME NOT NULL
	);

CREATE TABLE ordered_products(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	order_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	quantity INTEGER NOT NULL
);

CREATE TABLE products(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	name VARCHAR(128),
	category_id INTEGER NOT NULL,
	inventory_id INTEGER NOT NULL,
	total_price FLOAT NOT NULL
);

CREATE TABLE product_category(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	name VARCHAR(128) NOT NULL
);

CREATE TABLE inventory(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	quantity INTEGER NOT NULL,
	created_at DATETIME NOT NULL,
);

CREATE TABLE customers(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	first_name VARCHAR(128),
	last_name VARCHAR(128),
	email VARCHAR(128),
	telephone VARCHAR(128),
	address VARCHAR(256),
	postal_code VARCHAR(128),
	city_id INTEGER NOT NULL,
);


CREATE TABLE city(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	city_name VARCHAR(128),
	country_id INTEGER NOT NULL
);

CREATE TABLE country(
	id INTEGER IDENTITY(1,1) PRIMARY KEY,
	country_name CHAR(3)
);
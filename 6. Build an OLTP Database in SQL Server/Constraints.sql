-- CONSTRAINTS
USE RetailShopProject;

-- order_details table
ALTER TABLE order_details
	ADD CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers (id);


-- ordered_products table
ALTER TABLE ordered_products
	ADD CONSTRAINT fk_order_details FOREIGN KEY (order_id) REFERENCES order_details (id);

ALTER TABLE ordered_products
	ADD CONSTRAINT fk_products FOREIGN KEY (product_id) REFERENCES products (id);


-- products table
ALTER TABLE products
	ADD CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES product_category (id);

ALTER TABLE products
	ADD CONSTRAINT fk_inventory FOREIGN KEY (inventory_id) REFERENCES inventory (id);


-- customer_address table
ALTER TABLE customers
	ADD CONSTRAINT fk_city FOREIGN KEY (city_id) REFERENCES city (id);
ALTER TABLE customers
	ADD CONSTRAINT UQ_customers UNIQUE (email, telephone);


-- city table
ALTER TABLE city
	ADD CONSTRAINT fk_country FOREIGN KEY (country_id) REFERENCES country (id);

-- country table
ALTER TABLE country
	ADD CONSTRAINT UQ_country UNIQUE (country_name);


-- inventory table
ALTER TABLE inventory
	ADD CONSTRAINT CHK_quantity CHECK (quantity > 0);
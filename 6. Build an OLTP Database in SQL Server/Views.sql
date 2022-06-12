-- VIEW: virtual table that is not part of the physical schema
-- It stores a query in memory (but not the data)
USE RetailShopProject;

-- Access control: select the amount of sales made by clients for an specific country without granting access to customer sensitive data
GO
CREATE VIEW  dbo.sales_by_country (country_total_sales, country)  AS
	SELECT
		SUM(ord.total_price),
		cou.country_name
	FROM country cou
		INNER JOIN city ON cou.id = city.country_id
		INNER JOIN customers ON city.id = customers.city_id
		INNER JOIN order_details ord ON customers.id = ord.customer_id
	GROUP BY
		cou.country_name
;
GO

-- Views in the database
SELECT * FROM INFORMATION_SCHEMA.VIEWS;

-- Query the view
SELECT TOP(1) * FROM sales_by_country ORDER BY country_total_sales DESC;

-- Give access to the view
GRANT SELECT ON sales_by_country TO PUBLIC;


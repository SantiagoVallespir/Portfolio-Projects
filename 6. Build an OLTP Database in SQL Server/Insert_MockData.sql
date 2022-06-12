USE RetailShopProject;

BULK INSERT dbo.products
FROM 'C:\Users\santi\Desktop\Cursos datacamp\SQL Server for DBA\Capstone Project\mock data\products.csv'
WITH
(
        FORMAT='CSV',
        FIRSTROW=2
)
GO

SELECT * FROM products;
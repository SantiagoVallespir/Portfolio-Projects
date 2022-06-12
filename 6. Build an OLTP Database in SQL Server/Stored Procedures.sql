/* Stored procedures:
1. Add new country: cusp_AddNewCountry
2. Add new city: cusp_AddNewCity
3. Add new customer:
4. Add new order*/

USE RetailShopProject;

-- 1. Add new country: cusp_AddNewCountry
GO
CREATE PROCEDURE dbo.cusp_AddNewCountry (@CountryName VARCHAR(128))
AS
BEGIN
SET NOCOUNT ON

	BEGIN TRY
		BEGIN TRAN
			INSERT INTO country (country_name)
			VALUES (@CountryName)
			SELECT 
				'New country added to database' AS Message,
				country_name AS Added_country
			FROM country
			WHERE country_name = @CountryName
		COMMIT TRAN
	END TRY

	BEGIN CATCH
		SELECT 
			'Rolling back the transaction. The country exists into DB' AS Message,
			CAST(ERROR_NUMBER() AS VARCHAR) AS Error_Number,
			CAST(ERROR_SEVERITY() AS VARCHAR) AS Error_Severity,
			CAST(ERROR_STATE() AS VARCHAR) AS Error_state,
			ERROR_MESSAGE() AS Error_Message
		ROLLBACK TRAN;
	END CATCH

END;



-- 2. Add new city: cusp_AddNewCity
GO
CREATE PROCEDURE dbo.cusp_AddNewCity (@CityName VARCHAR(128), @Country_Name VARCHAR(128))
AS
BEGIN
SET NOCOUNT ON
	
	DECLARE @CountryID AS INT
	SET @CountryID = (SELECT id FROM country WHERE country_name = @Country_Name)
	
	IF @CountryID IS NULL
		BEGIN
			EXEC dbo.cusp_AddNewCountry
				@CountryName = @Country_Name
			SET @CountryID = (SELECT id FROM country WHERE country_name = @Country_Name)
		END

	ELSE
		BEGIN
			SET @CountryID = (SELECT id FROM country WHERE country_name = @Country_Name)
		END
	END

	BEGIN TRY
		BEGIN TRAN
			INSERT INTO city (city_name, country_id)
			VALUES (@CityName, @CountryID)
			SELECT 
				'New city added to database' AS Message,
				city_name AS Added_city
			FROM city
			WHERE city_name = @CityName
		COMMIT TRAN
	END TRY

	BEGIN CATCH
		SELECT 
			'Rolling back the transaction. The city exists into DB' AS Message,
			CAST(ERROR_NUMBER() AS VARCHAR) AS Error_Number,
			CAST(ERROR_SEVERITY() AS VARCHAR) AS Error_Severity,
			CAST(ERROR_STATE() AS VARCHAR) AS Error_state,
			ERROR_MESSAGE() AS Error_Message
			ROLLBACK TRAN;
	END CATCH
;
	

-- 3. Add new customer: cusp_AddNewCustomer
GO
CREATE PROCEDURE dbo.cusp_AddNewCustomer (
	@CityName VARCHAR(128), 
	@CountryName VARCHAR(128),
	@FirstName VARCHAR(128),
	@LastName VARCHAR(128),
	@Email VARCHAR(128),
	@Telephone VARCHAR(128),
	@Address VARCHAR(128),
	@PostalCode INT
	)
AS
BEGIN
SET NOCOUNT ON
	
	EXEC dbo.cusp_AddNewCountry
		@CountryName = @CountryName

	EXEC dbo.cusp_AddNewCity
		@Country_name = @CountryName,
		@CityName = @CityName

	DECLARE @CityID AS INT
	SET @CityID = (SELECT id FROM city WHERE city_name = @CityName)


	BEGIN TRY
		BEGIN TRAN
			INSERT INTO customers (first_name, last_name, email, telephone, address, postal_code, city_id)
			VALUES (@FirstName, @LastName, @Email, @Telephone, @Address, @PostalCode, @CityID)
			SELECT 
				'New customer added to database' AS Message,
				CONCAT(first_name, last_name) AS New_Customer
			FROM customers
			WHERE email = @Email
		COMMIT TRAN
	END TRY

	BEGIN CATCH
		SELECT 
			'Rolling back the transaction. The customer exists into DB' AS Message,
			CAST(ERROR_NUMBER() AS VARCHAR) AS Error_Number,
			CAST(ERROR_SEVERITY() AS VARCHAR) AS Error_Severity,
			CAST(ERROR_STATE() AS VARCHAR) AS Error_state,
			ERROR_MESSAGE() AS Error_Message
			ROLLBACK TRAN;
	END CATCH
END
;

-- 4. Add new order: dbo.cusp_AddOrder
GO
CREATE PROCEDURE dbo.cusp_AddOrder (
	@Email VARCHAR(128),
	@TotalPrice FLOAT,
	@Payment BIT
	)
AS
BEGIN
SET NOCOUNT ON
	
	-- Customer ID
	DECLARE @CustomerID AS INT
	SET @CustomerID = (SELECT id FROM customers WHERE email = @Email)

	-- Created At
	DECLARE @CreatedAt AS DATETIME
	SET @CreatedAt = GETDATE()

	BEGIN TRY
		BEGIN TRAN
			INSERT INTO order_details (customer_id, total_price, payment_status, created_at)
			VALUES (@CustomerID, @TotalPrice, @Payment, @CreatedAt)
			SELECT 
				'New order added to database' AS Message,
				id AS Order_ID
			FROM order_details
			WHERE id = SCOPE_IDENTITY()
		COMMIT TRAN
	END TRY

	BEGIN CATCH
		SELECT 
			'Rolling back the transaction. The Order exists into DB' AS Message,
			CAST(ERROR_NUMBER() AS VARCHAR) AS Error_Number,
			CAST(ERROR_SEVERITY() AS VARCHAR) AS Error_Severity,
			CAST(ERROR_STATE() AS VARCHAR) AS Error_state,
			ERROR_MESSAGE() AS Error_Message
		ROLLBACK TRAN;
	END CATCH

END;


-- 5. Add new ordered product: dbo.cusp_AddOrderedProduct
GO
CREATE PROCEDURE dbo.cusp_AddOrderedProduct(
	@Product VARCHAR(128),
	@Quantity FLOAT
	)

AS
BEGIN
SET NOCOUNT ON

	DECLARE @OrderID INT
	SET @OrderID = (SELECT MAX(id) FROM order_details)

	DECLARE @ProductTable TABLE(ProductID INT, InventoryID INT);
	INSERT INTO @ProductTable (ProductID, InventoryID) 
	SELECT TOP 1 id, inventory_id FROM products WHERE name = @Product ORDER BY inventory_id ASC;

	BEGIN TRY
		BEGIN TRAN
			INSERT INTO ordered_products (order_id, product_id, quantity)
			VALUES (@OrderID, (SELECT ProductID FROM @ProductTable), @Quantity)
			SELECT 'New products ordered associated to order' AS Message;
			
			UPDATE inventory
			SET quantity = quantity - @Quantity
			WHERE id = (SELECT InventoryID FROM @ProductTable);
		COMMIT TRAN
	END TRY

	BEGIN CATCH
		SELECT 
			'Rolling back the transaction. There are not products in inventory' AS Message,
			CAST(ERROR_NUMBER() AS VARCHAR) AS Error_Number,
			CAST(ERROR_SEVERITY() AS VARCHAR) AS Error_Severity,
			CAST(ERROR_STATE() AS VARCHAR) AS Error_state,
			ERROR_MESSAGE() AS Error_Message
		ROLLBACK TRAN;
	END CATCH
END
;


-- 6. Add full order transaction:
GO
CREATE PROCEDURE dbo.cusp_AddFullOrderTransaction(
	@Email VARCHAR(128),
	@TotalPrice FLOAT,
	@Payment BIT,
	@Product VARCHAR(128),
	@Quantity FLOAT
	)

AS
BEGIN
SET NOCOUNT ON

	EXEC dbo.cusp_AddOrder
	@Email = @Email,
	@TotalPrice = @TotalPrice,
	@Payment = @Payment;

	EXEC dbo.cusp_AddOrderedProduct
	@Product = @Product,
	@Quantity = @Quantity;


END
;


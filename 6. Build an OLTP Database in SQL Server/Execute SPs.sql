-- Execute transactions
EXEC dbo.cusp_AddNewCountry
	@CountryName = 'ITA'
;

EXEC dbo.cusp_AddNewCity
	@CityName = 'Roma',
	@Country_Name = 'ITA'
;

EXEC dbo.cusp_AddNewCustomer
	@CityName = 'Tandil', 
	@CountryName = 'ARG',
	@FirstName = 'Mario',
	@LastName = 'Vazquez',
	@Email = 'mariovazquez@gmail.com',
	@Telephone = '+54 9 11 3854-9685',
	@Address = 'Av. Malvinas Argentinas',
	@PostalCode = 1502
;

EXEC dbo.cusp_AddFullOrderTransaction
	@Email = 'juanperez@gmail.com',
	@TotalPrice = 10,
	@Payment = 1,
	@Product = 'short',
	@Quantity = 1
;

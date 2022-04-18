# Portfolio-Projects
Personal projects


# 1. Covid-19
We store covid data in a DBMS (SQL Server), we explore both within the database with sample Transact-SQL queries and we automate the actualization of the DB with new data.
### SQL competences showed:
- Build a DB
- Complex queries (CTE, Windows functions, views, joins, nested queries)
- Data modelling
### Python competences showed:
- Connect to a database
- Query the database
- Automate data loading into DB


# 2. Netflix movies Data Analysis project
Starting with a Netflix movies simple dataset i get data from another sources (TMDB, Instagram, IMDB) and i elaborate diverse metrics to understand which characteristics makes a high-rated movie and under what circumstances Netflix releases them.
### Competences showed:
- Web Scraping
- Exploratory data analysis/Data visualization
- Data wrangling
- Metric building
- Descriptive statistics
- OOP: develop ad-hoc programs, inheritance, polymorphism
- EDA


# 3. Statistics notebooks
Several notebooks i used while learning summary statistics, inferential statistics and probability

### 3.1. Hypothesis testing: click or not-click A/B test
In this simulated experiment, we try to discover if a modification in our company's advertisement can lead to an increase on its click-rate. We want to get an idea of how our new ad can increase the user's interest, and therefore increase the number of clicks.

To this reason, we simulate an ***A/B test*** in which 500 users are directed to the old ad (control group) and 500 users are directed to the new ad (test group). The test group will have a 48% click rate increase. We want to determine statistically whether that difference is due to chance or is statistically significant.

### 3.2. Descriptive statistics and probability.
In this notepad we try to get insigths about FIFA football international results from 1872 to 2022. The analysis is carried trying to answer the following questions:
- Is the number of goals increasing by match ever year?
- How total goals by match are distributed?
- What can we expect for next years?
- How frequently we can see a 10 or more goals match?
- How much we have to wait to see a 10 or more goals match?
- Home team is more likely to win?

#### Competences showed:
- EDA
- Probability distributions and modelling (Binomial, Poisson, Exponential)
- Bootstrapping
- Parameter Estimation


# 4. Tableau visualizations
Link: https://public.tableau.com/app/profile/santiago.vallespir7494#!/?newProfile=&activeTab=0

Some Tableau visualizations useful for Data Analytics

### 4.1. Choose your room!/AirBnB Rome
Choose your room!: interactive visualization of Rome's airbnb locations to choose a favourite one based on neighborhood, room type, nights and budget

Link: https://public.tableau.com/app/profile/santiago.vallespir7494/viz/ChooseyourRoom/ChooseyourRoom

AirBnB Rome: interactive dashboard with market estimate and potential revenues

Link:https://public.tableau.com/app/profile/santiago.vallespir7494/viz/AirbnbRoma_16245298983230/Stimadelmercatopotenzialiricavi

### 4.2 Winter olympics
Analytics dashboard with general performance on 2018 Winter Olympics

Link: https://public.tableau.com/app/profile/santiago.vallespir7494/viz/Winterolympics_16245278401520/Dashboard1

By country: https://public.tableau.com/app/profile/santiago.vallespir7494/viz/WinterOlympicsbycountry/Dashboard2


# 5. ETL process
The main idea is to apply an ETL (Extract, Transform and Load) process in a reduced scale, using python and handling diverse file formats (.csv, .json). 

The taks is to build a dataset containing the 50 biggest companies in the world by revenue including their revenue in diverse currencies (USD, EUR, GDP, JPY, BRL, ARS) and two columns with data from the company's country of origin.

To accomplish this task, the project is divided in three main sections:

**1. Extract**: data from different sources is collected and extracted into our local environment.
- **Web scraping:** a list of the 50 largest companies by revenue is scraped from Wikipedia using the library "Beautiful Soup".

Link: https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue

- **API communication:** the exchange rate from EUR to diverse currencies are downloaded in a .json format from "Exchange rates" api

Link: http://api.exchangeratesapi.io

- **Downloading datasets:** two datasets (population, gdp per capita) are downloaded from Gapminder.

Link: https://www.gapminder.org/data/

> Two different modules (***collect_data.py*** and ***etl_module.py***) are written to perform the operations on this section

**2. Transform:** some data manipulation operations are carried on to build the main .csv file
- Data cleaning
- Currency conversion
- Merging

**3. Load:*** export the resulting DataFrame to a unique .csv file called "final_dataset.csv".
> To load the dataset into a RDMBS data can be normalized.

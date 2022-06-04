# Portfolio-Projects
Personal projects


# 1. Covid-19: ETL process with Python and Data Analysis with SQL
The objective is to build a data pipeline that autonomously loads data related to Covid-19 in a PostgreSQL database. The data was taken from https://ourworldindata.org/ 

- **A. Create database:** we run the create_db.py script, which communicates with PostgreSQL and build a DB with two tables. It loads all data gathered until the 01/06/2022, the day the database was created.
- **B. Extract:** a new raw dataset is downloaded and stored locally
- **C.  Transform:** we get data we need excluding data that is already on the DB (filtering by date) and we prepare it to be consistent while loading. A new file ready to be loaded is saved locally.
- **D. Load:** we automate the loading into the DB.
- **E. Run ETL:** we execute the run_etl.py from bash run the process and load new data into DB.
- **F. Data Analysis with SQL:** we run a bunch of queries to analize the results

### Python competences showed:
- Creating a DB
- Automate data loading into DB
- OOP
- Automate a logfile
### SQL competences showed:
- Complex queries (CTE, Windows functions, joins, nested queries)
- Views
- Data modelling



# 2. Netflix movies Data Analytics project
Starting with a Netflix movies simple dataset i get data from another sources (TMDB, Instagram, IMDB) and i elaborate diverse metrics to understand which characteristics makes a high-rated movie and under what circumstances Netflix releases them.
### Competences showed:
- Web Scraping
- Exploratory data analysis/Data visualization
- Data wrangling
- Metric building
- Descriptive statistics
- OOP: develop ad-hoc programs, inheritance, polymorphism
- EDA


# 3. ETL process project
The main idea is to apply an ETL (Extract, Transform and Load) process in a reduced scale, using python and handling diverse file formats (.csv, .json). 

The taks is to build a dataset containing the 50 biggest companies in the world by revenue including their revenue in diverse currencies (USD, EUR, GDP, JPY, BRL, ARS) and two columns with data from the company's country of origin.

To accomplish this task, the project is divided in three main sections: Extract; Transform; Load
- **Extract:** the main data is scraped from https://www.wikipedia.org/, while the currencies are take taken from http://api.exchangeratesapi.io
- **Transform:** data is processed to build a main dataset integrating both data sources.
- **Load:** the dataset is saved locally in .csv format

### Competences showed:
- ETL
- Develop python modules
- Web scraping
- API's


# 4. Statistics notebooks
Several notebooks i used while learning summary statistics, inferential statistics and probability

### 4.1. Hypothesis testing: click or not-click A/B test
In this simulated experiment, we try to discover if a modification in our company's advertisement can lead to an increase on its click-rate. We want to get an idea of how our new ad can increase the user's interest, and therefore increase the number of clicks.

To this reason, we simulate an ***A/B test*** in which 500 users are directed to the old ad (control group) and 500 users are directed to the new ad (test group). The test group will have a 48% click rate increase. We want to determine statistically whether that difference is due to chance or is statistically significant.

### 4.2. Descriptive statistics and probability.
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


# 5. Tableau visualizations
Link: https://public.tableau.com/app/profile/santiago.vallespir7494#!/?newProfile=&activeTab=0

Some Tableau visualizations useful for Data Analytics

### 5.1. Choose your room!/AirBnB Rome
Choose your room!: interactive visualization of Rome's airbnb locations to choose a favourite one based on neighborhood, room type, nights and budget

Link: https://public.tableau.com/app/profile/santiago.vallespir7494/viz/ChooseyourRoom/ChooseyourRoom

AirBnB Rome: interactive dashboard with market estimate and potential revenues

Link:https://public.tableau.com/app/profile/santiago.vallespir7494/viz/AirbnbRoma_16245298983230/Stimadelmercatopotenzialiricavi

### 5.2 Winter olympics
Analytics dashboard with general performance on 2018 Winter Olympics

Link: https://public.tableau.com/app/profile/santiago.vallespir7494/viz/Winterolympics_16245278401520/Dashboard1

By country: https://public.tableau.com/app/profile/santiago.vallespir7494/viz/WinterOlympicsbycountry/Dashboard2

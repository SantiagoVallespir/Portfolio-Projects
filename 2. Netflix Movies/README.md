# Analyzing Netflix Movies data

The objective of the project is to draw conclusions from data collected from various sources refered to Netflix movies. To achieve this, we extract data from TMDB, IMDB and Instagram and we organize it in an structured file.

The process involves data collection, data manipulation and validation to test the quality of the data and to put it in a user friendly form. We follow the concept of "Tidy data" in which each row corresponds to an example of the sample and every column to one specific variable.

The final analysis is guided with some key questions that in particular try to get insights about the characteristics of the best ranked Netflix movies. The conclusions try to get understanding about which kind of Netflix products are performing better and in which products Neflix has to improve.

Besides, an ad-hoc python package ("Movie Pandas") built on Pandas was developed to automatize data collection, data cleaning and data manipulation for further analysis (as Netflix release new content every week)

## 1. Download data from TMDB

From an original Netflix movie's dataset (netflix_movies_dataset.xlsx) we connect to TMDB API and we download aditional data useful for its analysis.
Competences showed:
- Communicate with API's
- Data manipulation
- Data validation
- Data cleaning

## 2. Followers scraping

We automatize Google queries to get Instagram followers of the main cast (5 principal actors or actresses) of every movie. 
Competences showed:
- Web scraping
- Data cleaning

## 3. Build the DataFrame

We made the last validations of the data and we define the structure of the final DataFrame on wich the package is build. Besides, we build interesting new columns useful for the analysis.
Competences showed:
- Data cleansing
- Feature engineering


## 4. Netflix EDA

We realize the Exploratory Data Analysis of the dataset getting some insights about every single columns.
Competences showed:
- Data Visualization
- Descriptive statistics
- Exploratory data analysis

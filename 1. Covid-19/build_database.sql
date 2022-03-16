CREATE DATABASE covid_project;

USE covid_project;

CREATE TABLE countries(
	iso_code NCHAR(3) PRIMARY KEY NOT NULL,	
	continent NVARCHAR(20) NOT NULL,
	country NVARCHAR(50) NOT NULL,	
	population FLOAT NOT NULL,
	population_density FLOAT NULL,	
	median_age FLOAT NULL,
	aged_65_older FLOAT NULL,
	aged_70_older FLOAT NULL,
	gdp_per_capita FLOAT NULL,
	extreme_poverty FLOAT NULL,
	cardiovasc_death_rate FLOAT NULL,
	diabetes_prevalence FLOAT NULL,
	female_smokers FLOAT NULL,
	male_smokers FLOAT NULL,
	handwashing_facilities FLOAT NULL,
	hospital_beds_per_thousand FLOAT NULL,
	life_expectancy FLOAT NULL,
	human_development_index FLOAT NULL
);

CREATE TABLE covid_data(
	id FLOAT NOT NULL,
	iso_code NCHAR(3) FOREIGN KEY REFERENCES countries(iso_code) NOT NULL,
	date DATETIME NOT NULL,
	new_cases FLOAT NULL,
	new_deaths FLOAT NULL,
	icu_patients FLOAT NULL,
	hosp_patients FLOAT NULL,
	new_tests FLOAT NULL,
	positive_rate FLOAT NULL,
	people_vaccinated FLOAT NULL,	
	people_fully_vaccinated FLOAT NULL,	
	total_boosters FLOAT NULL,	
	new_vaccinations FLOAT NULL,
	excess_mortality FLOAT NULL
);

/* Replace 0 by null*/

UPDATE covid_data SET new_cases = NULL WHERE new_cases = 0;
UPDATE covid_data SET new_deaths = NULL WHERE new_deaths = 0;
UPDATE covid_data SET icu_patients = NULL WHERE icu_patients = 0;
UPDATE covid_data SET hosp_patients = NULL WHERE hosp_patients = 0;
UPDATE covid_data SET new_tests = NULL WHERE new_tests = 0;
UPDATE covid_data SET positive_rate = NULL WHERE positive_rate = 0;
UPDATE covid_data SET people_vaccinated = NULL WHERE people_vaccinated = 0;
UPDATE covid_data SET people_fully_vaccinated = NULL WHERE people_fully_vaccinated = 0;
UPDATE covid_data SET total_boosters = NULL WHERE total_boosters = 0;
UPDATE covid_data SET new_vaccinations = NULL WHERE new_vaccinations = 0;
UPDATE covid_data SET excess_mortality = NULL WHERE excess_mortality = 0;

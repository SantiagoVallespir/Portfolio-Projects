-- Select database
USE covid_project;

-- Select count distinct
SELECT 
	COUNT (DISTINCT iso_code) AS "different_countries"
FROM 
	covid_data;

-- Select days and countries with more new deaths (top 10)
SELECT 
	iso_code,
	date,
	new_deaths
FROM 
	covid_data
ORDER BY 
	new_deaths DESC
OFFSET 10 ROWS 
FETCH NEXT 10 ROWS ONLY;

-- Select countries with less than 100000 hab. and order by alphabet
SELECT
	country,
	population
FROM
	countries
WHERE
	population < 100000
ORDER BY
	country
;

-- Boosters in Argentina between january 2022 and february 2022
SELECT
	iso_code,
	date,
	total_boosters
FROM 
	covid_data
WHERE
	iso_code = 'ARG' AND
	date BETWEEN '2022/01/01 00:00:00' AND '2022/02/28 00:00:00'
ORDER BY 2
;

-- Select not null
SELECT 
	iso_code, 
	date, 
	new_deaths
FROM 
	covid_data
WHERE 
	new_deaths IS NOT NULL AND iso_code = 'ARG'
ORDER BY 2 DESC
;

-- Countries with higher percentage of population that got infected today
SELECT 
	cov.iso_code, 
	cov.new_cases, 
	cou.population, 
	ROUND((cov.new_cases / cou.population)*100,2) AS population_infected_percentage
FROM 
	covid_data AS cov
JOIN
	countries AS cou
ON
	cov.iso_code = cou.iso_code
WHERE 
	cov.date = '2022-03-12 00:00:00.000'
ORDER BY 4 DESC
;


-- Number of deaths by 100.000 by country in descending order
SELECT 
	cov.iso_code, 
	SUM(cov.new_deaths) as total_deaths, 
	cou.population, 
	SUM((cov.new_deaths/ cou.population)*100000) as deaths_by_100000hab
FROM 
	covid_data AS cov
JOIN
	countries AS cou
ON
	cov.iso_code = cou.iso_code
GROUP BY 
	cov.iso_code, 
	cou.population
ORDER BY 4 DESC
;

-- Death percentage in Italy
SELECT 
	iso_code,  
	SUM(new_deaths) AS total_deaths, 
	SUM(new_cases) AS total_cases, 
	ROUND((SUM(new_deaths) / SUM(new_cases)) *100, 2) AS death_percentage
FROM 
	covid_data
WHERE 
	iso_code = 'ITA'
GROUP BY
	iso_code
;

-- Death percentage: countries that starts with "G"
SELECT 
	iso_code,  
	SUM(new_deaths) AS total_deaths, 
	SUM(new_cases) AS total_cases, 
	ROUND((SUM(new_deaths) / SUM(new_cases)) *100, 2) AS death_percentage
FROM 
	covid_data
WHERE 
	iso_code LIKE 'G%'
GROUP BY
	iso_code
ORDER BY 4 DESC
;

-- Percentage of population tested positive(top 10)
SELECT
	cov.iso_code,
	cou.population,
	SUM(cov.new_deaths) AS total_deaths,
	ROUND((SUM(cov.new_deaths) / cou.population) *100, 3) AS percentage_of_population_dead
FROM
	covid_data AS cov
JOIN
	countries AS cou
ON
	cov.iso_code = cou.iso_code
GROUP BY
	cov.iso_code,
	cou.population
ORDER BY 4 DESC
OFFSET 10 ROWS 
FETCH NEXT 10 ROWS ONLY
;

-- Build a View to temporarily save data: deaths by 100000hab by country
CREATE VIEW deaths_per_100000hab AS
SELECT 
	cov.iso_code, 
	SUM(cov.new_deaths) AS total_deaths, 
	cou.population, 
	ROUND(SUM((cov.new_deaths / cou.population)*100000),2) as deaths_per_100000hab
FROM 
	covid_data AS cov
JOIN
	countries AS cou
ON
	cov.iso_code = cou.iso_code
GROUP BY cov.iso_code, cou.population
;

SELECT *
FROM deaths_per_100000hab
ORDER BY deaths_per_100000hab DESC
;

-- Build categories using CASE: we split the dataset by percentage of deaths by 100000hab.
SELECT 
	cov.iso_code, 
	SUM(cov.new_deaths) AS total_deaths, 
	cou.population, 
	ROUND(SUM((cov.new_deaths / cou.population)*100000),2) AS deaths_per_100000hab,
	CASE 
		WHEN ROUND(SUM((cov.new_deaths / cou.population)*100000),2)  < 50 THEN 'Low'
		WHEN ROUND(SUM((cov.new_deaths / cou.population)*100000),2)  BETWEEN 50 AND 150 THEN 'Medium'
		ELSE 'High' END
		AS level_death
FROM 
	covid_data AS cov
JOIN
	countries AS cou
ON
	cov.iso_code = cou.iso_code
GROUP BY 
	cov.iso_code, 
	cou.population
;

-- Having: select days with more than 3% of deaths by new cases
SELECT 
	date, 
	SUM(new_cases) AS world_new_cases, 
	SUM(new_deaths) AS world_new_deaths, 
	ROUND(SUM(new_deaths)/SUM(new_cases)*100,2) AS death_percentage 
FROM 
	covid_data
GROUP BY 
	date
HAVING 
	SUM(new_deaths)/SUM(new_cases)*100 > 3
ORDER BY 1
;

-- Partition by: vaccination accumulated in Brazil by 7 days
SELECT 
	cov.iso_code, 
	cov.date, 
	cou.population, 
	cov.new_vaccinations, 
	SUM(cov.new_vaccinations) OVER(
									PARTITION BY 
										cov.iso_code 
									ORDER BY 
										cov.date
									ROWS BETWEEN 7 PRECEDING AND CURRENT ROW) AS vaccinations_cumulated
FROM 
	covid_data AS cov
JOIN 
	countries AS cou
ON 
	cov.iso_code = cou.iso_code
WHERE
 cov.iso_code = 'BRA'
ORDER BY 2 
;

-- CTE: Add percemtage of vaccinations (single dose) respect to population to a table
WITH PopvsVac 
	(iso_code, 
	date, 
	population, 
	new_vaccinations, 
	vaccinations_cumulated)
AS
(
SELECT 
	cov.iso_code, 
	cov.date, 
	cou.population, 
	cov.new_vaccinations, 
	SUM(cov.new_vaccinations) OVER(
									PARTITION BY 
										cov.iso_code 
									ORDER BY 
										cov.iso_code, 
										cov.date) AS vaccinations_cumulated
FROM 
	covid_data AS cov
JOIN 
	countries AS cou
ON 
	cov.iso_code = cou.iso_code
)

SELECT 
	*, 
	(vaccinations_cumulated/population)*100 AS percentage_vaccinations_population
FROM 
	PopvsVac
WHERE
 iso_code = 'ESP'
;

 -- TEMP TABLE: add percentage of vaccinated population (one dose)
DROP TABLE IF EXISTS #PopvsVac
CREATE TABLE #PopvsVac
(
Location NVARCHAR(3),
Date DATETIME,
Population NUMERIC,
New_vaccinations NUMERIC,
Vaccinations_cumulated NUMERIC
)

INSERT INTO 
	#PopvsVac
SELECT 
	cov.iso_code, 
	cov.date, 
	cou.population, 
	cov.new_vaccinations, 
	SUM(cov.new_vaccinations) OVER (
									PARTITION BY 
										cov.iso_code 
									ORDER BY 
										cov.date) AS vaccinations_cumulated
FROM 
	covid_data AS cov
JOIN 
	countries AS cou
ON 
	cov.iso_code= cou.iso_code

SELECT 
	*, 
	(vaccinations_cumulated/population)*100 AS percentage_vaccinations_population
FROM 
	#PopvsVac
WHERE
	Location ='ROU'
;

-- CTE + Sub-query in Select: compare deadths by 100000hab by country with world mean
WITH deaths_by_country (
	location, 
	total_deaths, 
	population, 
	deaths_per_100000hab) AS
(
SELECT 
	cov.iso_code, 
	SUM(cov.new_deaths) AS total_deaths, 
	cou.population, 
	ROUND((SUM(new_deaths) / population)*100000,2) AS deaths_per_100000hab
FROM 
	covid_data AS cov
JOIN
	countries AS cou
ON
	cov.iso_code = cou.iso_code
GROUP BY 
	cov.iso_code, 
	cou.population
)

SELECT 
	*,
	(SELECT 
		SUM(total_deaths)/SUM(population)*100000 
	 FROM 
		deaths_by_country) AS world_average,
	CASE 
		WHEN deaths_per_100000hab < (SELECT 
								         SUM(total_deaths)/SUM(population)*100000 
	                                 FROM 
		                                 deaths_by_country) THEN 'Low'
		ELSE 
			'High' END AS 
				level_death
FROM 
	deaths_by_country
ORDER BY 
	deaths_per_100000hab DESC
;

-- Add column with relationshipo between country's mean and world's mean
WITH deaths_by_country (
	location, 
	total_deaths, 
	population, 
	deaths_per_100000hab) AS
(
SELECT 
	cov.iso_code, 
	SUM(cov.new_deaths) AS total_deaths, 
	cou.population, 
	ROUND((SUM(new_deaths) / population)*100000,2) AS deaths_per_100000hab
FROM 
	covid_data AS cov
JOIN
	countries AS cou
ON
	cov.iso_code = cou.iso_code
GROUP BY 
	cov.iso_code, 
	cou.population
)

SELECT 
	*,
	(SELECT 
		SUM(total_deaths)/SUM(population)*100000 
	 FROM 
		deaths_by_country) AS world_average,
	deaths_per_100000hab - (SELECT 
								SUM(total_deaths)/SUM(population)*100000 
							FROM 
								deaths_by_country) AS diff_avg
FROM 
	deaths_by_country
ORDER BY 
	deaths_per_100000hab DESC
;

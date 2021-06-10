
/*
Covid-19 Data Exploration

Skills: Gestione dei dati (nomi delle colonne, cast di datatypes), Joins, CTE's, View, Window Functions, Aggregate Functions, Sub-queries, Case.
USE covid_19;
*/

USE covid_19;

--- Rinominare le colonne
EXECUTE sp_RENAME 'covid_deaths.date', 'day_of_year', 'COLUMN';
EXECUTE sp_RENAME 'covid_vaccinations.date', 'day_of_year', 'COLUMN';

-- Modificare il datetype se necessario
ALTER TABLE covid_deaths ALTER COLUMN total_deaths INT;
ALTER TABLE covid_deaths ALTER COLUMN new_deaths INT;
ALTER TABLE covid_deaths ALTER COLUMN total_deaths_per_million FLOAT;
ALTER TABLE covid_deaths ALTER COLUMN new_deaths_per_million FLOAT;
ALTER TABLE covid_deaths ALTER COLUMN reproduction_rate FLOAT;
ALTER TABLE covid_deaths ALTER COLUMN icu_patients INT;

-- Controllare i cambi 
SELECT * 
FROM covid_deaths
ORDER BY 3,4;

SELECT * 
FROM covid_vaccinations
ORDER BY 3,4;


-- Selezionare i dati
SELECT location, day_of_year, total_cases, new_cases, total_deaths, population
FROM covid_deaths
WHERE continent is not null
ORDER BY 1,2;


-- Total cases vs. total deaths
SELECT location, day_of_year, total_cases, total_deaths, (total_deaths / total_cases)*100 AS death_percentage
FROM covid_deaths
WHERE location = 'Italy'
ORDER BY 1,2;


-- Total cases vs. total deaths: paesi che cominciano con "United"
SELECT location, day_of_year, total_cases, total_deaths, (total_deaths / total_cases)*100 AS death_percentage
FROM covid_deaths
WHERE location LIKE 'United%'
ORDER BY 1,2;


-- Total cases vs. population: percentuale della popolazione testata positiva
SELECT location, day_of_year, total_cases, population, (total_cases / population)*100 AS population_infected_percentage
FROM covid_deaths
WHERE location = 'Argentina'
ORDER BY 1,2;


-- Paesi con la percentuale della popolazione infettata più alta al giorno di oggi
SELECT location, total_cases, population, (total_cases / population)*100 AS population_infected_percentage
FROM covid_deaths
WHERE day_of_year = '2021-06-07 00:00:00.000' AND continent is not null
ORDER BY population_infected_percentage DESC;


-- Numero di morti per 100.000 abitanti per paese in ordine decrescente
SELECT location, MAX(total_deaths) as max_total_deaths, population, MAX((total_deaths / population)*100000) as morti_per_100000hab
FROM covid_deaths
WHERE continent is not null
GROUP BY location, population
ORDER BY morti_per_100000hab DESC;


-- Costruire una view per salvare i dati più tardi
CREATE VIEW DeathsPerCountryPerc AS
SELECT location, MAX(total_deaths) as max_total_deaths, population, MAX((total_deaths / population)*100000) as morti_per_100000hab
FROM covid_deaths
WHERE continent is not null
GROUP BY location, population;


-- Costruire categorie utilizzando CASE: splitiamo il dataset secondo la percentuale di morti per 100.000 ab.
SELECT location, MAX(total_deaths) as max_total_deaths, population, MAX((total_deaths / population)*100000) as morti_per_100000hab,
CASE WHEN MAX((total_deaths / population)*100000) < 50 THEN 'Low'
	WHEN MAX((total_deaths / population)*100000) BETWEEN 50 AND 150 THEN 'Medium'
	ELSE 'High' END
	AS level_death
FROM covid_deaths
WHERE continent is not null
GROUP BY location, population
ORDER BY morti_per_100000hab DESC;

-- Numero di morti per 100.000 abitanti per continente in ordine decrescente
SELECT location, MAX(total_deaths) as max_total_deaths, population, MAX((total_deaths / population)*100000) as morti_per_100000hab
FROM covid_deaths
WHERE continent is null
GROUP BY location, population
ORDER BY morti_per_100000hab DESC;


-- Numeri globali
-- Totale di nuovi casi e nuovi morti per giorno in tutto il mondo
SELECT day_of_year, SUM(new_cases) as world_new_cases, SUM(new_deaths) as world_new_deaths, SUM(new_deaths)/SUM(new_cases)*100 AS deat_percentage 
FROM covid_deaths
WHERE continent is not null
GROUP BY day_of_year
ORDER BY day_of_year ASC;


-- Selezionare i giorni con più del 3% di morti per nuovi casi
SELECT day_of_year, SUM(new_cases) AS world_new_cases, SUM(new_deaths) AS world_new_deaths, SUM(new_deaths)/SUM(new_cases)*100 AS death_percentage 
FROM covid_deaths
WHERE continent is not null
GROUP BY day_of_year
HAVING SUM(new_deaths)/SUM(new_cases)*100 > 3
ORDER BY day_of_year;


-- Totali accumulati di vaccinazioni per paese: Window Function
SELECT dea.continent, dea.location, dea.day_of_year, dea.population, vac.new_vaccinations, SUM(CAST(vac.new_vaccinations as INT))  
OVER (PARTITION BY dea.location ORDER BY dea.location, dea.day_of_year) AS vaccinations_cumulated
FROM covid_deaths AS dea
JOIN covid_vaccinations AS vac
	ON dea.location = vac.location
	AND dea.day_of_year = vac.day_of_year
WHERE dea.continent is not null
ORDER BY 2,3


-- Aggiungere la percentuale delle vaccinazioni rispetto alla popolazione alla tabella utilizzando una CTE
WITH PopvsVac (continent, location, day_of_year, population, new_vaccinations, vaccinations_cumulated)
AS
(
SELECT dea.continent, dea.location, dea.day_of_year, dea.population, vac.new_vaccinations, SUM(CAST(vac.new_vaccinations as INT))  
OVER (PARTITION BY dea.location ORDER BY dea.location, dea.day_of_year) AS vaccinations_cumulated
FROM covid_deaths AS dea
JOIN covid_vaccinations AS vac
	ON dea.location = vac.location
	AND dea.day_of_year = vac.day_of_year
WHERE dea.continent is not null
)
SELECT *, (vaccinations_cumulated/population)*100 AS percentage_vaccinations_population
FROM PopvsVac


-- Aggiungere il percentuale della popolazione vaccinata almeno con una dosi alla tabella utilizzando una TEMP TABLE
DROP TABLE IF EXISTS #PopvsVac
CREATE TABLE #PopvsVac
(
Continent NVARCHAR(255),
Location NVARCHAR(255),
Day_of_Year DATETIME,
Population NUMERIC,
New_vaccinations NUMERIC,
Vaccinations_cumulated NUMERIC
)

INSERT INTO #PopvsVac
SELECT dea.continent, dea.location, dea.day_of_year, dea.population, vac.new_vaccinations, SUM(CAST(vac.new_vaccinations as INT))  
OVER (PARTITION BY dea.location ORDER BY dea.location, dea.day_of_year) AS vaccinations_cumulated
FROM covid_deaths AS dea
JOIN covid_vaccinations AS vac
	ON dea.location = vac.location
	AND dea.day_of_year = vac.day_of_year
WHERE dea.continent is not null

SELECT *, (vaccinations_cumulated/population)*100 AS percentage_vaccinations_population
FROM #PopvsVac


-- Confrontare i dati di morti per 100.000 per paese con la media mondiale: CTE e Sub-query in SELECT
WITH deaths_by_country (location, max_total_deaths, population, deaths_per_100000hab) AS
(
SELECT location, MAX(total_deaths) as max_total_deaths, population, MAX((total_deaths / population)*100000) as deaths_per_100000hab
FROM covid_deaths
WHERE continent is not null
GROUP BY location, population
)
SELECT *,
	(SELECT SUM(max_total_deaths)/SUM(population)*100000 
	FROM deaths_by_country) AS world_average
FROM deaths_by_country
ORDER BY deaths_per_100000hab DESC;


-- Aggiungere colonna con il rapporto della media del paese con la media del mondo per 100.000ab
WITH deaths_by_country (location, max_total_deaths, population, deaths_per_100000hab) AS
(
SELECT location, MAX(total_deaths) as max_total_deaths, population, MAX((total_deaths / population)*100000) as deaths_per_100000hab
FROM covid_deaths
WHERE continent is not null
GROUP BY location, population
)
SELECT *,
	(SELECT SUM(max_total_deaths)/SUM(population)*100000 
	FROM deaths_by_country) AS world_average,
	deaths_per_100000hab - (SELECT SUM(max_total_deaths)/SUM(population)*100000 
	FROM deaths_by_country) AS diff_avg
FROM deaths_by_country
ORDER BY deaths_per_100000hab DESC;

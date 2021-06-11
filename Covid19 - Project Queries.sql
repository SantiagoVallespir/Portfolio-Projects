USE covid_19;

ALTER TABLE covid_vaccinations ALTER COLUMN total_vaccinations INT;
ALTER TABLE covid_vaccinations ALTER COLUMN total_tests INT;
ALTER TABLE covid_vaccinations ALTER COLUMN new_tests INT;

SELECT * FROM covid_deaths;
SELECT * FROM covid_vaccinations;


-- Numeri totali 
WITH tot_num AS
(
SELECT dea.continent, dea.location, dea.population, MAX(dea.total_cases) AS total_cases, MAX(dea.total_deaths) AS total_deaths, 
MAX(CAST(vac.total_tests AS BIGINT)) AS total_tests, MAX(CAST(vac.total_vaccinations AS BIGINT)) AS total_vaccinations
FROM covid_deaths AS dea
JOIN covid_vaccinations AS vac
	ON dea.iso_code = vac.iso_code
WHERE dea.continent IS NOT NULL AND vac.continent IS NOT NULL
GROUP BY dea.continent, dea.location, dea.population
) 
SELECT SUM(population) AS total_population, SUM(total_cases) AS total_cases, SUM(total_deaths) AS total_deaths, 
SUM(total_tests) AS total_tests, SUM(total_vaccinations) AS total_vaccinations
FROM tot_num;


-- Numeri per continenti
WITH tot_num AS
(
SELECT dea.continent, dea.location, dea.population, MAX(dea.total_cases) AS total_cases, MAX(dea.total_deaths) AS total_deaths, 
MAX(CAST(vac.total_tests AS BIGINT)) AS total_tests, MAX(CAST(vac.total_vaccinations AS BIGINT)) AS total_vaccinations
FROM covid_deaths AS dea
JOIN covid_vaccinations AS vac
	ON dea.iso_code = vac.iso_code
WHERE dea.continent IS NOT NULL AND vac.continent IS NOT NULL
GROUP BY dea.continent, dea.location, dea.population
) 
SELECT continent, SUM(population) AS total_population, SUM(total_cases) AS total_cases, SUM(total_deaths) AS total_deaths, 
SUM(total_tests) AS total_tests, SUM(total_vaccinations) AS total_vaccinations
FROM tot_num
GROUP BY continent;


-- Numeri per paesi
SELECT dea.continent, 
	   dea.location, 
	   dea.population, 
	   vac.population_density, 
	   vac.median_age, 
	   vac.aged_65_older, 
	   vac.gdp_per_capita,
	   vac.diabetes_prevalence, 
	   vac.handwashing_facilities, 
	   vac.hospital_beds_per_thousand, 
	   vac.life_expectancy, 
	   vac.human_development_index,
	   MAX(dea.total_cases) AS total_cases,
	   MAX(dea.total_deaths) AS total_deaths,
	   MAX(vac.total_tests) AS total_tests,
	   MAX(vac.total_vaccinations) AS total_vaccinations,
	   ROUND(MAX((dea.total_cases)/dea.population*100), 2, 0) AS cases_percentage_pop,
	   ROUND(MAX((dea.total_cases)/dea.population*100000), 2, 0) AS cases_percentage_pop_hab,
	   ROUND(MAX((dea.total_deaths)/dea.population*100), 2, 0) AS deaths_percentage_pop,
	   ROUND(MAX((dea.total_deaths)/dea.population*100000), 2, 0) AS deaths_percentage_pop_hab,
	   ROUND(MAX((vac.total_tests)/dea.population*100), 2, 0) AS tests_percentage_pop,
	   ROUND(MAX((vac.total_tests)/dea.population*100000), 2, 0) AS tests_percentage_pop_hab,
	   ROUND(MAX((vac.total_vaccinations)/dea.population*100), 2, 0) AS vaccinations_percentage_pop,
	   ROUND(MAX((vac.total_vaccinations)/dea.population*100000), 2, 0) AS vaccinations_percentage_pop_hab
FROM covid_deaths AS dea
JOIN covid_vaccinations AS vac
	ON dea.iso_code = vac.iso_code 
	AND dea.location = vac.location
WHERE dea.continent IS NOT NULL AND vac.continent IS NOT NULL
GROUP BY dea.location,
		 dea.continent,
		 dea.population,
		 vac.population_density, 
	     vac.median_age, 
	     vac.aged_65_older, 
	     vac.gdp_per_capita,
		 vac.diabetes_prevalence, 
	     vac.handwashing_facilities, 
	     vac.hospital_beds_per_thousand,
		 vac.life_expectancy, 
	     vac.human_development_index
ORDER BY dea.location ASC;


-- Numeri totali
SELECT dea.continent, 
	   dea.location, 
	   dea.population,
	   dea.day_of_year,
	   vac.population_density, 
	   vac.median_age, 
	   vac.aged_65_older, 
	   vac.gdp_per_capita,
	   vac.diabetes_prevalence, 
	   vac.handwashing_facilities, 
	   vac.hospital_beds_per_thousand, 
	   vac.life_expectancy, 
	   vac.human_development_index,
	   dea.new_cases,
	   dea.total_cases,
	   dea.new_deaths,
	   dea.total_deaths,
	   vac.total_tests,
	   (dea.total_cases/dea.population)*100 AS cases_percentage_pop,
	   (dea.total_cases/dea.population)*100000 AS cases_percentage_pop_hab,
	   (dea.total_deaths/dea.population)*100 AS deaths_percentage_pop,
	   (dea.total_deaths/dea.population)*100000 AS deaths_percentage_pop_hab,
	   (vac.total_tests/dea.population)*100 AS tests_percentage_pop,
	   (vac.total_tests/dea.population)*100000 AS tests_percentage_pop_hab,
	   (vac.total_vaccinations/dea.population*100) AS vaccinations_percentage_pop,
	   (vac.total_vaccinations/dea.population*100) AS vaccinations_percentage_pop_hab
FROM covid_deaths AS dea
JOIN covid_vaccinations AS vac
	ON dea.iso_code = vac.iso_code 
	AND dea.location = vac.location
WHERE dea.continent IS NOT NULL AND vac.continent IS NOT NULL
ORDER BY dea.location ASC, dea.day_of_year ASC;




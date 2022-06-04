from sqlalchemy import create_engine, Column, Integer, Date, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from utils import load_file, log
from datetime import datetime


# Local variables
path = r"C:\Users\santi\Desktop\Portfolio-Projects-main\1. Covid-19\data\covid_2022_01_06.csv"
engine = create_engine("postgresql+psycopg2://postgres:aa11bb22cc@localhost:5432/covid_project")
Base = declarative_base()


class Countries(Base):
    
	__tablename__ = "Countries"

	id = Column(Integer, autoincrement=True, unique=True, nullable=False)
	iso_code = Column(String(3), primary_key=True, nullable=False)
	continent = Column(String(20), nullable=False)
	country = Column(String(50), nullable=False)
	population = Column(Float)
	population_density = Column(Float)	
	median_age = Column(Float)
	aged_65_older = Column(Float)
	aged_70_older = Column(Float)
	gdp_per_capita = Column(Float)
	extreme_poverty = Column(Float)
	cardiovasc_death_rate = Column(Float)
	diabetes_prevalence = Column(Float)
	female_smokers = Column(Float)
	male_smokers = Column(Float)
	handwashing_facilities = Column(Float)
	hospital_beds_per_thousand = Column(Float)
	life_expectancy = Column(Float)
	human_development_index = Column(Float)


class CovidData(Base):

    __tablename__ = "CovidData"

    id = Column(Integer, primary_key=True, nullable=False)
    iso_code = Column(String(3), ForeignKey("Countries.iso_code"), nullable=False)
    date = Column(Date, nullable=False)
    new_cases = Column(Float)
    new_deaths = Column(Float)
    icu_patients = Column(Float)
    hosp_patients = Column(Float)
    new_tests = Column(Float)
    positive_rate = Column(Float)
    people_vaccinated = Column(Float)
    people_fully_vaccinated = Column(Float)
    total_boosters = Column(Float)
    new_vaccinations = Column(Float)
    excess_mortality = Column(Float)


def prepare_country_data(df):
    """Function that prepares data to be loaded into the Countries table on the DB
    
    Args:
        df (pandas.Datafame): pandas.DataFrame to be cleaned
        
    Returns:
        countries_data_clean (pandas.DataFrame): pandas.DataFrame cleaned and ready to be loaded into Countries table"""

    df.rename(columns={"location": "country"}, inplace=True)

    # countries data
    countries_data = df[[
                    "iso_code",
                    "continent",
                    "country",
                    "population",
                    "population_density",
                    "median_age",
                    "aged_65_older",
                    "aged_70_older",
                    "gdp_per_capita",
                    "extreme_poverty",
                    "cardiovasc_death_rate",
                    "diabetes_prevalence",
                    "female_smokers",
                    "male_smokers",
                    "handwashing_facilities",
                    "hospital_beds_per_thousand",
                    "life_expectancy",
                    "human_development_index"
                    ]].copy()

    # delete unseful_data
    to_delete = ["OWID_AFR",
            "OWID_ASI",
            "OWID_EUR",
            "OWID_EUN",
            "OWID_HIC",
            "OWID_INT",
            "OWID_KOS",
            "OWID_LIC",
            "OWID_LMC",
            "OWID_NAM",
            "OWID_CYN",
            "OWID_OCE",
            "OWID_SAM",
            "OWID_UMC",
            "OWID_WRL"
           ]

    countries_data_clean = countries_data[~countries_data["iso_code"].isin(to_delete)]       
    countries_data_clean = countries_data_clean.drop_duplicates()
    
    # "id" column
    countries_data_clean.reset_index(drop=True, inplace=True)
    countries_data_clean["id"] = countries_data_clean.index
    cols = countries_data_clean.columns.to_list()
    cols = cols[-1:] + cols[:-1]
    countries_data_clean = countries_data_clean[cols]
    
    # data validation
    if len(countries_data_clean['iso_code'].unique()) != 229:
        raise ValueError('Countries must be 229!')

    return countries_data_clean


def prepare_covid_data(df):
    """Function that prepares data to be loaded into the CovidData table on the DB
    
    Args:
        df (pandas.Datafame): pandas.DataFrame to be cleaned
        
    Returns:
        covid_data_clean (pandas.DataFrame): pandas.DataFrame cleaned and ready to be loaded into CovidData table"""
    
    df.rename(columns={"location": "country"}, inplace=True)

    # covid_data
    covid_data = df[[
                "iso_code", 
                "date",
                "new_cases",
                "new_deaths",
                "icu_patients",
                "hosp_patients",
                "new_tests",
                "positive_rate",
                "people_vaccinated",
                "people_fully_vaccinated",
                "total_boosters",
                "new_vaccinations",
                "excess_mortality"
             ]].copy()
    
    # delete unseful_data
    to_delete = ["OWID_AFR",
            "OWID_ASI",
            "OWID_EUR",
            "OWID_EUN",
            "OWID_HIC",
            "OWID_INT",
            "OWID_KOS",
            "OWID_LIC",
            "OWID_LMC",
            "OWID_NAM",
            "OWID_CYN",
            "OWID_OCE",
            "OWID_SAM",
            "OWID_UMC",
            "OWID_WRL"
           ]

    covid_data_clean = covid_data[~covid_data["iso_code"].isin(to_delete)]
    
    # "id" column
    covid_data_clean.reset_index(drop=True, inplace=True)
    covid_data_clean["id"] = covid_data_clean.index
    cols = covid_data_clean.columns.to_list()
    cols = cols[-1:] + cols[:-1]
    covid_data_clean = covid_data_clean[cols]

     # "date" column
    covid_data_clean["date"] = [datetime.strptime(row, "%d/%m/%Y") for row in covid_data_clean["date"]]

    # data validation
    if len(covid_data_clean['iso_code'].unique()) != 229:
        raise ValueError('Countries must be 229!')

    return covid_data_clean

def load_data_to_db(path):
	"""Function that connects to the DB, processes the data and loads it to DB
    
    Args:
        path (str)"""

	df = load_file(path, sep=";")

	# Both tables data
	countries = prepare_country_data(df)
	covid = prepare_covid_data(df)

	# Load data
	connection = engine.connect()
	countries.to_sql(name="Countries", con=connection, if_exists="append", index=False)
	covid.to_sql(name="CovidData", con=connection, if_exists="append", index=False)
	connection.close()
	engine.dispose()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    load_data_to_db(path)
    log("The DB was created")
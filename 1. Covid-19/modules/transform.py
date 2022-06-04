import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from utils import load_file, log


def prepare_data(df):
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
    covid_data_clean["date"] = [datetime.strptime(row, "%Y-%m-%d") for row in covid_data_clean["date"]]

    # data validation
    if len(covid_data_clean['iso_code'].unique()) != 229:
        raise ValueError('Countries must be 229!')

    return covid_data_clean

def get_last_date(connection):
    """Gets in input a DB connection and returns last date actualized on DB
    
    Args:
        connection (sqlalchemy.engine.base.Connection): connection to DB
        
    Returns:
        date (datetime.date): last date actualized on DB"""
    
    stmt = 'SELECT MAX(date) FROM "CovidData"'
    date = connection.execute(stmt).fetchall()
    
    return date[0][0]


def get_index(connection):
    """Gets in input a DB connection and returns the biggest id on CovidData table
        
        Args:
            connection (sqlalchemy.engine.base.Connection): connection to DB
            
        Returns:
            counter (int): biggest id on CovidData"""
    
    stmt = 'SELECT MAX(id) FROM "CovidData"'
    index = connection.execute(stmt).fetchall()
    counter = int(index[0][0])
    
    return counter


def transform_data(path, connection):
    """Takes the new csv and extract new rows not loaded on DB

    Args:
        path (str): path to .csv file
        connection (sqlalchemy.engine.base.Connection): connection to DB
    
    Returns:
        new_covid (pandas.DataFrame): new DataFrame ready to be loaded into the DB"""
    
    # Load and prepare data
    df = load_file(path, sep=",")
    new_covid = prepare_data(df)
    
    last_date = get_last_date(connection)
    counter = get_index(connection)

    # Select rows
    new_covid["date"] = [row.date() for row in new_covid["date"]]
    new_covid = new_covid[new_covid["date"] > last_date]

    # Build index
    new_covid["id"] = np.arange(counter+1, counter+1+len(new_covid))
    new_covid.reset_index(drop=True, inplace=True)
    
    # Columns
    # cols = new_covid.columns.to_list()
    # cols = cols[-1:] + cols[:-1]
    # new_covid = new_covid[cols]

    return new_covid

def make_new_csv(path, connection, new_path):
    """Save a clean .csv file ready to be loaded into db
    
    Args:
        path (str): path to .csv file
        connection (sqlalchemy.engine.base.Connection): connection to DB
        new_path (str): path to save the new file"""
    
    df = transform_data(path, connection)
    df.to_csv(new_path, sep=",", index=False)
    log("Data transformed ready to be loaded")


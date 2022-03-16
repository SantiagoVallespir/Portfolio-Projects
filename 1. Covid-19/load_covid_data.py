import urllib.request
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pyodbc

url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
path = "owid-covid.csv"


# Make connection with DB
engine = create_engine('mssql+pyodbc://LAPTOP-R1I2JR4H\SQLEXPRESS/covid_project?driver=SQL+Server+Native+Client+11.0')
connection = engine.connect()


def download_file(url, filename):
    '''Connects with the server and download data as csv'''
    response = urllib.request.urlopen(url)    
    file = open(filename + ".csv", "wb")
    file.write(response.read())
    file.close()
    

def prepare_data(path):
    '''Takes the file, transform it to pd.DataFrame and prepare it for our needs'''
    df = pd.read_csv(path, sep=',')
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
    to_delete= ["OWID_AFR",
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
    covid_data_clean.reset_index(drop=True, inplace=True)
    
    if len(covid_data_clean['iso_code'].unique()) != 223:
        raise ValueError('Countries must be 223!')
    
    # date column
    covid_data_clean["date"] = covid_data_clean["date"].apply(pd.to_datetime)

    return covid_data_clean


def get_last_date(connection):
    '''Return last date actualized on DB'''
    stmt = "SELECT MAX(date) FROM covid_data"
    date = connection.execute(stmt).fetchall()
    last_date = int(date[0][0])
    return last_date


def get_index(connection):
    '''Return max(id) from db'''
    stmt = "SELECT MAX(id) FROM covid_data"
    index = connection.execute(stmt).fetchall()
    counter = int(index[0][0])
    return counter


def make_new_csv(df):
    '''Takes old csv as pd.DataFrame a make a new one with data not loaded into DB'''
    last_date = get_last_date(connection)
    counter = get_index(connection)

    # Select rows
    df = df[df["date"] > last_date]

    # Index
    df["id"] = np.arange(counter+1, counter+1+len(df))
    # Columns
    cols = df.columns.to_list()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    # Make a new file
    df.to_csv(r"C:\Users\santi\Desktop\Portfolio-Projects-main\Covid project\covid_data_new.csv",
                sep=",",
                header=False,
                index=False)

    

download_file(url, "owid-covid")
make_new_csv(prepare_data(path))

# Load data and close connection
df = pd.read_csv(r"C:\Users\santi\Desktop\Portfolio-Projects-main\Covid project\covid_data_new.csv")
df.to_sql(name="covid_data", con=connection, if_exists="append", index=False)
connection.close()
engine.dispose()

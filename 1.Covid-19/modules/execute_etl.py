from sqlalchemy import create_engine
import extract
import transform
import load


url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
extract_path = r"C:\Users\santi\Desktop\Portfolio-Projects-main\1. Covid-19\data\covid_2022_03_06"
transform_path = r"C:\Users\santi\Desktop\Portfolio-Projects-main\1. Covid-19\data\covid_2022_03_06.csv"
new_path = r"C:\Users\santi\Desktop\Portfolio-Projects-main\1. Covid-19\data\covid_2022_03_06_clean.csv"
load_path = r"C:\Users\santi\Desktop\Portfolio-Projects-main\1. Covid-19\data\covid_2022_03_06_clean.csv"

engine = create_engine("postgresql+psycopg2://postgres:aa11bb22cc@localhost:5432/covid_project")

if __name__ == "__main__":
    extract.extract(url, extract_path)
    connection = engine.connect()
    transform.make_new_csv(transform_path, connection, new_path)
    load.load_clean_data(load_path, connection)
    connection.close()
    engine.dispose()
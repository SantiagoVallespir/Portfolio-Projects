from utils import load_file, log
from sqlalchemy import create_engine

def load_clean_data(path, connection):
    """Connects to the DB an load the clean .csv file
    
    Args:
        path (str): path to .csv file
        connection (sqlalchemy.engine.base.Connection): connection to DB"""

    df = load_file(path, sep=",")

    # Load data
    df.to_sql(name="CovidData", con=connection, if_exists="append", index=False)

    # Print message
    log("Data loaded into DB")
   

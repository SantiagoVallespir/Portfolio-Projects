from datetime import datetime
import pandas as pd

def log(message):
    """Function that takes a message in input and prints a log event.
    It actualizes a 'logfile.txt' that takes a record of all processes that have been made
    
    Args:
        message(string)"""
    
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now() 
    timestamp = now.strftime(timestamp_format)
    with open(r"C:\Users\santi\Desktop\Portfolio-Projects-main\1. Covid-19\data\logfile.txt","a") as f:
        f.write(timestamp + ', ' + message + '\n')
    print(timestamp + ', ' + message + '\n')

def load_file(path, sep):
    """Takes the downloaded .csv file and imports it as a pd.DataFrame
    
    Args:
        path (str): path to the covid-19 .csv file
        sep (str): separator between rows
        
    Returns:
        df (pandas.Dataframe): .csv file transformed to pd.Dataframe"""

    df = pd.read_csv(path, sep=sep)
    
    return df
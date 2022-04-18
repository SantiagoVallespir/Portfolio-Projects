# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 11:03:29 2022

@author: santi
"""

import glob
import pandas as pd
from datetime import datetime

def extract_csv(file, sep):
    """Function that takes a csv file in input and transforms it to a pandas.DataFrame
    
    Args:
        file (file): csv file to extract
        sep (str): csv delimitator
        
    Returns:
        pandas.DataFrame"""
    
    df = pd.read_csv(file, sep=sep, index_col = 0)
    
    return df


def extract(file, columns, sep):
    """Function that iterates on all csv files saved locally and applies 'extract_csv' function 
    to the file specified on input. 
    It returns a DataFrame with the columns in input.
    
    Args:
        file (str): csv file name
        columns (list): list of columns that pandas.DataFrame will have
        sep (str): csv delimitator
        
    Returns:
        pandas.DataFrame"""
    
    for csvfile in glob.glob("*.csv"):
        df = extract_csv(f"{file}.csv", sep = sep)
        
    for old_column, new_column in zip(df.columns, columns):
        df = df.rename(columns = {old_column: new_column})

    return df


def load(df, name):
    """Function that takes a pandas.DataFrame as input and save it locally to csv with a name
    in input
    
    Args:
        df (pandas.DataFrame)
        name (str): name of the new csv file
        
    Return:
        file: save the csv locally"""
    
    return df.to_csv(f"{name}.csv", index=False)


def log(message):
    """Function that takes a message in input and prints a log event.
    It actualizes a 'logfile.txt' that takes a record of all processes that have been made
    
    Args:
        message(string)"""
    
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now() 
    timestamp = now.strftime(timestamp_format)
    with open("logfile.txt","a") as f:
        f.write(timestamp + ', ' + message + '\n')
    print(timestamp + ', ' + message + '\n')
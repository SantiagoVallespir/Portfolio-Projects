# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 10:43:18 2022

@author: santi
"""


from bs4 import BeautifulSoup
import requests
import pandas as pd

def scraper(url):
    """Function that takes and ULR on input, scrape data requested and returns
    the result in a HTML text format
    
    Args:
        url (str): URL adress.
    
    Returns:
        bs4.BeautifulSoup: HTML text"""
        
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
        
    return soup


def talk_to_api(key, csv_name):
    """Function that communicates with http://api.exchangeratesapi.io API, and 
    get EUR conversion rate to all the currencies on their database in JSON format.
    It makes a DataFrame with every currency as the index and a 'rates' column and it saves
    it locally with 'csv_name' as input.
    
    Args:
        key (str): key to communicate to the API.
        csv_name (str): name of the DataFrame to be saved locally.
        
    Returns:
        status_code"""
    
    url = f"http://api.exchangeratesapi.io/v1/latest?base=EUR&access_key={key}"
    
    data = requests.get(url)
    json = data.json()
    df = pd.DataFrame(json)
    df = df.drop(columns=["success", "timestamp","base","date"])
    df["rates"] = round(df["rates"],3)
    
    df.to_csv(f"{csv_name}.csv")
    
    print("Status code (if 200 then success): ", data.status_code)
    
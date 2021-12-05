# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 15:23:12 2021

@author: Santiago
"""

import requests
import pandas as pd
from scrapy import Selector

def get_male_cast(movie_id):
    '''
    Gets a movie id and get the sum of male actors in the movie
    
    Parameters
    ==========
    
    movie_id: int
        Movie's ID
    
    Returns
    =======
    int
        Sum of male actors
    '''
    
    # Connect with the API
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=f062d4d3bef1ed6f224531125e4c20c7&language=en-US")

    # Save the cast in a list
    cast = list(response.json()["cast"])
    
    # Sum of male actors
    male_actors = 0
    
    ## Loop that builds the sum of male actors
    for actor in cast:
        if actor["gender"] == 2:
            male_actors += 1
        else:
            pass
        
    # Return the sum
    return male_actors

def get_female_cast(movie_id):
    '''
    Gets a movie id and get the sum of female actors in the movie
    
    Parameters
    ==========
    
    movie_id: int
        Movie's ID
    
    Returns
    =======
    int
        Sum of female actors
    '''
    
    # Connect with the API
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=f062d4d3bef1ed6f224531125e4c20c7&language=en-US")

    # Save the cast in a list
    cast = list(response.json()["cast"])
    
    # Sum of male actors
    female_actors = 0
    
    ## Loop that builds the sum of male actors
    for actor in cast:
        if actor["gender"] == 1:
            female_actors += 1
        else:
            pass
        
    # Return the sum
    return female_actors
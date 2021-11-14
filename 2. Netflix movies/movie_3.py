import requests
import movie_2

def get_movie_data(movie_id, *args):
    '''
    Takes a movie ID and a list of useful movie data we need, connects with TMDB API, requests the data and it returns
    the data required.
    
    Parameters
    ==========
    
    movie_id: int 
        movie's id we use to connect to the API
    
    *args: str 
        details we want to get
        
    Returns
    =======
    
    list 
        list with the field required passed in *args
    
    >>> The details can be found here: https://developers.themoviedb.org/3/movies/get-movie-details'''
    
    
    # Connect with the API
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f062d4d3bef1ed6f224531125e4c20c7")
    
    # Make list of details with a for iteration calling the keys in args
    details= []
    for detail in args:
        try:
            details.append(response.json()[detail])
        except:
            details.append("?")
    
    return details
"""
Created on Sun Nov 14 17:07:12 2021

@author: Ospite
"""


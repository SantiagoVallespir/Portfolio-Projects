import movie_1
import datetime
import pandas as pd

def get_movie_id(title, release_year):
    '''
    Function that takes in input a movie title and its release year, communicates with TMDB API and returns the ID of
    the movie that matches the release year of the title in input
    
    Parameters
    ==========

    title: str 
        movie's title
    
    release_year: int 
        movie's release year
    
    Returns
    =======
    
    int 
        movie's id
    '''
    
    # Applies get_movie_data function to get data about every movie with a same title
    data = movie_1.get_movie(title)
    
    # Make a for cicle to return de ID of the movie that matches the year in input or the year before (teather's premiere)
    try:
        if len(data) == 1:
            return data[0]["id"]
        
        elif len(data) > 1:
            for i in data:
                date = pd.to_datetime(i["release_date"])
                if release_year == date.year or release_year == (date.year) + 1:
                    return i["id"]
                else:
                    pass
        
        else:
            pass
        
    # If the program can't find the release_date returns "?"
    except:
        return "?"
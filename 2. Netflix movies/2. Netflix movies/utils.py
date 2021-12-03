import requests
import pandas as pd

def get_movie(title):
       
        # Prepare the string for the ID query replacing " " for "%20"
        title.replace(" ", "%20")
    
        # Communicate with the API
        response = requests.get(f"http://api.tmdb.org/3/search/movie?api_key=f062d4d3bef1ed6f224531125e4c20c7&query={title}")
    
        # If the status_code is 200 the function communicated correctly with the API
        if response.status_code == 200:
            
            #Gets movie's data and returns it
            try:
                movie_data = response.json()['results']
                
                return movie_data
        
            # If the program can't get data it prints a phrase
            except:
                raise Exception("No data was found")
    
        else:
            raise Exception("The program failed to communicate with the API")



def get_movie_id(title, release_year):
        
    # Applies get_movie_data function to get data about every movie with a same title
    data = get_movie(title)
        
    # Make a for cicle to return de ID of the movie that matches the year in input or the year before (teather's premiere)
    try:
        if len(data) == 1:
            return int(data[0]["id"])
            
        elif len(data) > 1:
            for i in data:
                date = pd.to_datetime(i["release_date"])
                if release_year == date.year or release_year == (date.year) + 1:
                    return int(i["id"])
                else:
                    pass
        
        else:
            pass
        
    # If the program can't find the release_date returns "?"
    except:
        return None
    
def get_movie_data(movie_id, column):
    '''
    Takes a movie ID and a list of useful movie data we need. 
    
    Connects with TMDB API and requests the data 
    
    Returns the data required.
    
    Parameters
    ==========
    
    movie_id: int 
        movie's id we use to connect to the API
    
    columns: list of str 
        details we want to get
        
    >>> Possible *args:
        
        > adult (bool)
        > backdrop_path (str or null)
        > belongs_to_collection (obj or null)
        > budget (int)
        > genres (obj)
        > homepage (str or null)
        > id (int)
        > imdb_id (str or null)
        > original_language (str)
        > original_title (str)
        > overview (str or null)
        > popularity (float)
        > poster_path (str or null)
        > production_companies (obj)
        > production_countries (obj)
        > release_date (str)
        > revenue (int)
        > runtime (int or null)
        > spoken_languages (obj)
        > status (str)
        > tagline (str)
        > title (str)
        > video (bool)
        > vote_average (float)
        > vote_count (int)
        
    Returns
    =======
    
    list 
        list with the field required passed in *args
    
    >>> The details can be found here: https://developers.themoviedb.org/3/movies/get-movie-details'''
    
    
    # Connect with the API
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f062d4d3bef1ed6f224531125e4c20c7")
    
    # Make list of details with a for iteration calling the keys in args
    
    return response.json()[column]
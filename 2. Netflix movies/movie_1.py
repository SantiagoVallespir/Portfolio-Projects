import requests

def get_movie(movie):
    '''
    
    Function that gets the name of the movie, connects with the TMDB API and gets all movies data with same name
    
    Parameters
    ==========
    
    movie: str
        Movie's name
    
    Returns
    =======
    
    dict
        movie's data
    '''
    
    # Prepare the string for the ID query replacing " " for "%20"
    movie.replace(" ", "%20")
    
    # Communicate with the API
    response = requests.get(f"http://api.tmdb.org/3/search/movie?api_key=f062d4d3bef1ed6f224531125e4c20c7&query={movie}")
    
    # If the status_code is 200 the function communicated correctly with the API
    if response.status_code == 200:
        
        #Gets movie's data and returns it
        try:
            movie_data = response.json()['results']
        
            return movie_data
        
        # If the program can't get data it prints a phrase
        except:
            movie_data = "No data was found"
            
            return movie_data
    
    else:
        return "The program failed to communicate with the API"

import requests
import pandas as pd
from scrapy import Selector
import urllib
from requests_html import HTML
from requests_html import HTMLSession


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



def get_imdb_score(imdb_id):
        
        # Communicate with the API
        response = requests.get(f"https://www.imdb.com/title/{imdb_id}").content
    
       
        sel = Selector(text = response)
        xpath='//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text()'
            
        return float(sel.xpath(xpath).extract()[0])
    
def get_cast(movie_id):
    # Connect with the API
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=f062d4d3bef1ed6f224531125e4c20c7&language=en-US")
    
    # Save the cast and crew in respective lists
    cast = list(response.json()["cast"])
    crew = list(response.json()["crew"])
    
    # List to fullfill
    actor_list = []
    directors = []
    
    ## Loop that creates a list with the original name of every actor (if actor is relevant)
    for actor in cast:
        if actor["gender"] != 0:
            actor_list.append(actor["original_name"])
        else:
            pass
        
        
    ## Get the director
    for person in crew:
        if person["job"] == "Director":
            directors.append(person["original_name"])
        else:
            pass
        
        
    return actor_list, directors


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


# First function: to pass our URL to Requests-HTML and return the source code of the page.
def get_source(url):
    
    session = HTMLSession()
    # Make a response object with the URL
    response = session.get(url)
    return response

# Second function: to format and URL encode the query, send it to Google and show the output.
def get_results(query):
    
    # Safe mode for quoting the URL replacing special characters
    query = urllib.parse.quote_plus(query)
    # Once the query is "safe" apply the get_source function
    response = get_source("https://www.google.com/search?q=" + query + " instagram")
    
    return response

# Third function: to get results
def parse_results(response):

    # Select elements with CSS selectors; the CSS can change in the future
    css_identifier_title = "h3"
    css_identifier_result = ".tF2Cxc"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)
    
    output = []
    
    for result in results:

        try:
            item = {'text': result.find(css_identifier_text, first=True).text,
                   'title': result.find(css_identifier_title, first=True).text}
        
            output.append(item)
        
        except:
            output.append("")
        
    return output[0]

# Fourth function: to print result
def google_search(query):
    response = get_results(query)
    
    try:
        result = parse_results(response)
    
        return result
    
    except:
        
        return ""
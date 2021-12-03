# CLASS INHERITANCE PANDAS
# FUNCION LLENAR DATAFRAME (HACERLO CON METODO O DEFINIENDOLO DE UNA SERIE)

import requests
import pandas as pd
import numpy as np


class MovieTable(pd.DataFrame):
    
    @classmethod
    def load_file(cls, filename):
        df = pd.read_csv(filename)
        if len(df.columns) > 2:
            raise Exception("The DataFrame must have two columns")
        else:
            return cls(df)
            return print(df)
    @classmethod
    def single_movie(cls, movie, year):
        data = [[movie, year]]
        df = pd.DataFrame(data, columns = ['movie', 'year'])
        return cls(df)
        return print(df)
        
    @property
    def _constructor(self, *args, **kwargs):
        pd.DataFrame._constructor(self, *args, **kwargs)
        return MovieTable

    @property
    def get_movie(movie):
        '''
        Function that takes the name of the movie, connects with the TMDB API 
        and gets all movies data with same name
    
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
                raise Exception("No data was found")
    
        else:
            raise Exception("The program failed to communicate with the API")

    
    @property
    def get_movie_id(title, release_year):
        '''
        Function that takes in input a movie title and its release year, communicates 
        with TMDB API and returns the ID of the movie that matches the release year 
        of the title in input
        
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
        
        (None)
            if program failed to get the id
            '''
    
        # Applies get_movie_data function to get data about every movie with a same title
        data = MovieTable.get_movie(title)
        
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


    @property    
    def get_movie_data(movie_id, columns):
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
        details= {}
        for detail in columns:
            try:
                details[detail] = response.json()[detail]
            except:
                details[detail] = None
                    
        return details


    def run_pipeline(df):
        '''
        Function that takes a DataFrame with movie and release year.
        
        Connects with the TMDB API.
        
        Request the data entered as input.
        
        Makes a list with the data cycling for every movie and year.
        
        Parameters
        ==========
    
        file (pd.DataFrame):
            DataFrame with "movie" column and "year"
    
        Returns
        =======
    
        details: list of dicts
            List with every single column requested and respective data
        '''
    
        # Movies and year lists: checks the data type and fulfill variables
        movies = None
        years = None

        if file.dtypes[0] == object:
            movies = list(file.iloc[:, 0])
            years = list(file.iloc[:, 1])
        else:
            movies = list(file.iloc[:, 1])
            years = list(file.iloc[:, 0])

        # Make a zip iterator with te movie and respective year
        movie_year = zip(movies, years)    
    
        # Get columns to require   
        columns = []

        i = ''
        while i != 'q':
            i = str(input("Enter data or press 'q' to exit: "))
            if i != 'q':
                columns.append(i)
            else:
                break

        # Apply "get_movie_id" for every tuple in "movie_year"
        movie_ids = [get_movie_id(pair[0], pair[1]) for pair in movie_year]

        # Get data for every movie with "get_movie_data"    
        details = []
        for movie_id in movie_ids:
            details.append(get_movie_data(movie_id, columns))
    
        return details


    def flatten_json(y):
  
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    if a != 'id':
                        flatten(x[a], name + a + '_')
                    else:
                        pass
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return pd.json_normalize(out)

# Make the DataFrame
'''def make_df(file):
    
    data = run_pipeline(file)
    
    if len(data) == 1:
        
        return flatten_json(data)
    
    else:
        
        df = flatten_json(data[0])
        
        #for movie in data[1:]:
         #   pd.concat([df, movie], axis = 1, ignore_index = True)
            
        #return df.to_csv("df.csv", index = False)
        return df
    

flatten_json(run_pipeline(file))
'''
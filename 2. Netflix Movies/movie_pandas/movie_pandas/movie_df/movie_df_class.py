# Import pandas as pd
import pandas as pd
from datetime import datetime
import numpy as np
from ..utils import get_movie, get_movie_id, get_movie_data, get_imdb_score, get_cast, get_male_cast, get_female_cast, get_source, get_results, parse_results, google_search
import requests
from scrapy import Selector
import urllib
from requests_html import HTML
from requests_html import HTMLSession

class MovieDF(pd.DataFrame):
    
    @classmethod
    def load_file(cls, filename):
        df = pd.read_csv(filename)
        if len(df.columns) > 2:
            raise Exception("The DataFrame must have two columns")
        else:
            return cls(df)
            return print(df)
    
    @classmethod
    def single_movie(cls, title, year):
        data = [[title, year]]
        df = pd.DataFrame(data, columns = ['title', 'year'])
        return cls(df)
        return print(df)
    
    def __init__(self, *args, **kwargs):
        pd.DataFrame.__init__(self, *args, **kwargs)
        self.created_at = datetime.today()
        self.order = [
                      "tmdb_id",
                      "imdb_id",
                      "title",
                      "original_title",
                      "release_date",
                      "year",
                      "month",
                      "year/month",
                      "weekday",
                      "original_language",
                      "runtime",
                      "genres_1",
                      "genres_2",
                      "production_countries_1",
                      "production_countries_2",
                      "overview",
                      "cast",
                      "director",
                      "male_actors",
                      "female_actors",
                      "total_actors",
                      "gender_difference",
                      "vote_count",
                      "vote_average",
                      "followers",
                      "imdb_score",
                     ]
    
    @property
    def get_id_column(self):
        columns = self.columns
        iterator = zip(self[columns[0]], self[columns[1]])
        self["tmdb_id"] = [get_movie_id(x[0], x[1]) for x in iterator]
        return self
    
    
    def add_new_column(self, column_name):   
        self[column_name] = [get_movie_data(x, column_name) for x in self["tmdb_id"]]
        return self
    
    def add_new_columns(self, columns_names):
        if type(columns_names) != list:
            raise Exception("Must enter list of column names")
        else:
            for column in columns_names:
                self[column] = [get_movie_data(x, column) for x in self["tmdb_id"]]
            return self
    
    @property
    def make_date_columns(self):
        self['release_date']= pd.to_datetime(self['release_date'])
        
        # Column 'Month'
        self['month'] = self.release_date.dt.month

        # Convert the results to string
        self['month'] = self['month'].replace(1, 'january')
        self['month'] = self['month'].replace(2, 'february')
        self['month'] = self['month'].replace(3, 'march')
        self['month'] = self['month'].replace(4, 'april')
        self['month'] = self['month'].replace(5, 'may')
        self['month'] = self['month'].replace(6, 'june')
        self['month'] = self['month'].replace(7, 'july')
        self['month'] = self['month'].replace(8, 'august')
        self['month'] = self['month'].replace(9, 'september')
        self['month'] = self['month'].replace(10, 'october')
        self['month'] = self['month'].replace(11, 'november')
        self['month'] = self['month'].replace(12, 'december')
        
        # Column 'year/month'
        self['year/month'] = self.release_date.apply(lambda dt: dt.replace(day=1))
        
        # Column 'weekday'
        self['weekday'] = self.release_date.dt.weekday

        # Convert the results to string
        self['weekday'] = self['weekday'].replace(0, 'monday')
        self['weekday'] = self['weekday'].replace(1, 'tuesday')
        self['weekday'] = self['weekday'].replace(2, 'wednesday')
        self['weekday'] = self['weekday'].replace(3, 'thursday')
        self['weekday'] = self['weekday'].replace(4, 'friday')
        self['weekday'] = self['weekday'].replace(5, 'saturday')
        self['weekday'] = self['weekday'].replace(6, 'sunday')
        
        return self
    
    def flat_column(self, column):
        
        i = 0
        genres_list = []

        for row in self[column]:
            row_genres = []
            for genre in row:
                row_genres.append(genre["name"])
            genres_list.append(row_genres)
            i += 1
    
        self[column + "_1"] = [row[0] for row in genres_list]
        
        column_2 = []
        
        for row in genres_list:
            try:
                column_2.append(row[1])
            except:
                column_2.append(None)
                
        self[column + "_2"] = column_2      
        
        self.drop(columns = column, axis = 1, inplace = True)
        
        return self
    
    @property
    def get_score_column(self):
        self["imdb_score"] = [get_imdb_score(x) for x in self["imdb_id"]]
        return self
    
    @property
    def get_cast_director(self):
        self["cast"] = [get_cast(x)[0] for x in self["tmdb_id"]]
        self["director"] = [get_cast(x)[1] for x in self["tmdb_id"]]
        return self
    
    @property
    def get_cast_columns(self):
        self["male_actors"] = [get_male_cast(x) for x in self["tmdb_id"]]
        self["female_actors"] = [get_female_cast(x) for x in self["tmdb_id"]]
        self["total_actors"] = self["male_actors"] + self["female_actors"]
        self["gender_difference"] = self["male_actors"] - self["female_actors"]
        
        # Clean "gender_difference" column
        self = self.astype({"gender_difference":"float64"})
        for x in range(len(self)):
            if self.iloc[x,-2] == 0:
                self.iloc[x,-1] = None
            else:
                pass
        
        return self
    
    @property
    def main_cast(self):
        '''Takes the cast_column and returns a main cast list with the first 5 actors if possible'''
        main_cast = self["cast"].tolist()
        main_cast_list = []

        for cast in main_cast:
            actors_clean = []
            for actor in cast:
                actors_clean.append(actor.strip())
            main_cast_list.append(actors_clean)

        main_cast_final = []

        for cast in main_cast_list:
            if len(cast) < 5:
                main_cast_final.append(cast)
            else:
                main_cast_final.append(cast[0:5])

        return main_cast_final
    
    @property
    def get_followers(self):
        followers = []

        for cast in self.main_cast:
            followers_x = []
            for actor in cast:
                result = google_search(actor)
                followers_x.append(result["text"])
            followers.append(followers_x)
            
        # Clean followers
        followers_clean = []

        for cast in followers:
            clean = []
            for actor in cast:
                text = actor.split(" ")
                clean.append(text[0])
            followers_clean.append(clean)

        # Build the column
        self["followers"] = followers_clean

        return self
    
    @property
    def clean_followers_column(self):
        followers = self["followers"].tolist()
        
        # Hundred of thousands
        n = 0
        for lista in followers:
            x = 0
            for i in lista:
                if len(i) == 4:
                    followers[n][x] = (i.replace("k", "000"))
                    x += 1
                else:
                    x +=1
            n += 1   
            
        # Thousands
        n = 0
        for lista in followers:
            x = 0
            for i in lista:
                followers[n][x] = (i.replace("k", "00"))
                x += 1
            n += 1
        
        # Millions
        n = 0
        for lista in followers:
            x = 0
            for i in lista:
                if len(i) <= 3:
                    followers[n][x] = (i.replace("m", "000000"))
                    x += 1
                else:
                    x +=1
            n += 1
            
        # Cast everything to integer
        n = 0
        for lista in followers:
            x = 0
            for i in lista:
                try:
                    followers[n][x] = int(i)
                    x += 1
                except:
                    followers[n][x] = 0
                    x += 1
            n += 1    

        # Build the column
        self["followers"] = [sum(row) for row in followers]
        
        return self
    
    @property
    def order_columns(self):
        self = self[self.order]
        return self
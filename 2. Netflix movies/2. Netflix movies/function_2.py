import pandas as pd
from function_1 import get_movie

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
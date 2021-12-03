import requests

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

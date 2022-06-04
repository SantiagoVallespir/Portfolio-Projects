import urllib.request
from utils import log


def download_file(url):
    """Connects with the server and download data as csv
    
    Args:
        url (str): url to requests.
    
    Returns:
        response (requests.Response): requests.Response object containing the content of the HTTP request. 
    """
    response = urllib.request.urlopen(url)    

    return response


def save_file(path, response):
    """Saves locally the content of a HTTP request as filename.csv
    
    Args:
        path (str): path where filename.csv will be saved.
        response (requests.Response):  requests.Response object containing the content of the HTTP request to save on filename.csv
    """

    file = open(path + ".csv", "wb")
    file.write(response.read())
    file.close()


def extract(url, path):
    """Extract datae and save it to a .csv file.
    
    Args:
        path (str): path where filename.csv will be saved.
        url (str): url to requests."""

    try:
        response = download_file(url)
        save_file(path, response)
        print(log("Data extracted"))
        
    except:
        print("The extraction raised an error!!")

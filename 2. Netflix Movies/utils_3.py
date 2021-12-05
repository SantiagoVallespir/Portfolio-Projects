# Import the libraries
import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

# First function: to pass our URL to Requests-HTML and return the source code of the page.
def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTML response object from requests_html. 
    """
    
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

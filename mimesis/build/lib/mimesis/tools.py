#
import requests
from typing import Union
from requests import Response
#from bs4 import BeautifulSoup

def get_response(url: str, timeout: int = 10) -> Union[tuple[None, str], tuple[Response, None]]:
    """Get the response from a URL
    Args:
        url (str): The URL to get the response from
        timeout (int): The timeout for the HTTP request
    Returns:
        tuple[None, str] | tuple[Response, None]: The response and error message
    Raises:
        ValueError: If the URL is invalid
        requests.exceptions.RequestException: If the HTTP request fails
    """

    session = requests.Session()

    try:
        response = session.get(url, timeout=timeout)

        # Check if the response contains an HTTP error
        if response.status_code >= 400:
            return None, f"Error: HTTP {str(response.status_code)} error"

        return response, None
    except ValueError as ve:
        # Handle invalid URL format
        return None, f"Error: {str(ve)}"

    except requests.exceptions.RequestException as re:
        # Handle exceptions related to the HTTP request
        #  (e.g., connection errors, timeouts, etc.)
        return None, f"Error: {str(re)}"

def scrape_text(url: str) -> str:
    """Scrape text from a webpage
    Args:
        url (str): The URL to scrape text from
    Returns:
        str: The scraped text
    """
    response, error_message = get_response(url)
    if error_message:
        return error_message
    if not response:
        return "Error: Could not get response"

    #soup = BeautifulSoup(response.text, "html.parser")
    soup = {}

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 0]
    chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
    text = "\n".join(chunk for chunk in chunks if chunk)

    #if len(list(lines)):
    #    if self.website == "theguardian":
    #        self.title = list(lines)[0].split("|")[0].strip()

    return text

def load_headlines(db = "/Users/nico/Code/klog/data/llm/apps/library/articles.duckdb"):
    import duckdb
    con = duckdb.connect(database=db)
    headlines = con.sql("""SELECT "title" FROM articles_newsapi WHERE date = '2023-06-10'""").to_df()
    return headlines
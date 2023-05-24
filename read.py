import requests
import logging
from actions import Action
from agent import Agent
from requests import Response
from bs4 import BeautifulSoup

class ReadWebsite(Action):

    #session.headers.update({"User-Agent": CFG.user_agent})
    name: str = "Website reader"
    description: str = "Website reader"
    definition: str = """You can read. When you read, you generate thoughts. Thoughts are brief sentences that relate your personality traits with the text that you are reading. You should always write thoughts in the following format: Thought: "thought". These are examples of thoughts:
* Thought: I find black holes very interesting, but I don't know much about them, I should read more.
* Thought: I wonder how people feel when dying, and if I could experience something similar.
"""
    url: str
    website: str | None = None
    title: str | None = None

    #@validate_url
    def get_response(
        self, url: str, timeout: int = 10
    ) -> tuple[None, str] | tuple[Response, None]:
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

    def scrape_text(self) -> str:
        """Scrape text from a webpage
        Args:
            url (str): The URL to scrape text from
        Returns:
            str: The scraped text
        """
        response, error_message = self.get_response(self.url)
        if error_message:
            return error_message
        if not response:
            return "Error: Could not get response"

        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 0]
        chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
        text = "\n".join(chunk for chunk in chunks if chunk)

        if len(list(lines)):
            if self.website == "theguardian":
                self.title = list(lines)[0].split("|")[0].strip()

        return text

    def memory(self, agent: Agent) -> str:
        if self.website == "theguardian":
            return f"I read the following article from The Guardian: {self.title}"
        else:
            return f"I read the following article: {self.url}"

    def do(self, agent: Agent) ->  str:
        logging.warning(f"Reading website: {self.url}")
        article: str = self.scrape_text()
        return f"""{self.definition}

Read the following article, delimited by triple equal signs. After reading the article, provide an enumerated list of 5 thoughts:
===
{article}
===
"""
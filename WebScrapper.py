import requests
from bs4 import BeautifulSoup
import validator_collection.validators as validators


class WebScrapper:
    """

    """

    def __init__(self, url) -> None:
        self._url = validators.url(url, allow_empty=False)
        pass

    def set_url(self, url):
        self._url = validators.url(url, allow_empty=False)

    def scrape(self):
        self._request = requests.get(self._url)
        self._soup = BeautifulSoup(self._request.text, 'html.parser')
        return self._soup

    def get_soup(self):
        return self._soup

    # def make_request(self, url):
    #     """Summary:

    #     Makes an HTTP GET request to the provided URL and returns a parsed HTML object for easier data access

    #     Throws Exceptions if URL is invalid; or req can't be resolved

    #     Args:
    #         URL_path (str): URL that has to match a regex fitler (structure: https://www.example.com)

    #     Returns:
    #         BeautifulSoup: object that represents a parsed HTML document
    #     """

    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

    #     URL = validators.url(URL_path, allow_empty=False)
    #     req = requests.get(URL, headers=headers)
    #     soup = BeautifulSoup(req.text, 'html.parser')
    #     return soup

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

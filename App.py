import configparser
import requests
from bs4 import BeautifulSoup
import re

import validator_collection.validators as validators

# configuration settings from .ini file
config = configparser.ConfigParser()
config.read('config.ini')


def retrieve_web_page(URL_path: str):
    """Summary:

    Makes an HTTP GET request to the provided URL and returns a parsed HTML object for easier data access

    Throws Exceptions if URL is invalid; or req can't be resolved

    Args:
        URL_path (str): URL that has to match a regex fitler (structure: https://www.example.com)

    Returns:
        BeautifulSoup: object that represents a parsed HTML document
    """

    URL = validators.url(URL_path, allow_empty=False)
    req = requests.get(URL)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup


def extract_data(soup: BeautifulSoup) -> tuple[str, str]:
    """Summary

    Uses the HTML parser to extract title and description

    Args:
        soup (BeautifulSoup: Object): HTML parser

    Returns:
        (title: str, description: str) -> tuple
    """
    title = soup.head.title.string if soup.head.title else 'No title available'

    # atribut name de forma description sau Description; optional incepe cu og:
    regex_pattern = re.compile('[og:]?[d|D]escription')
    meta = soup.head.find(
        'meta', attrs={'name': regex_pattern})

    description = meta['content'] if meta else 'No description available'

    return title, description


def get_URL_from_keyboard() -> str:
    """
        Prompts the user to enter a URL with a structure similar to: https://www.example.com

    Returns:
        str: validated URL
    """
    is_valid = False
    URL = None
    while not is_valid:
        try:
            URL_str = input("Enter your URL: ")
            URL = validators.url(URL_str)
            is_valid = True
        except validators.errors.InvalidURLError:
            print("Please provide a valid URL")

    return URL


if __name__ == '__main__':
    # # 1) Scrieti un script care deschide un URL specificat de la tastatura si printeaza titlul paginii HTML si description meta
    # URL = get_URL_from_keyboard()
    # soup = retrieve_web_page(URL)
    # title, description = extract_data(soup)
    # print(title)
    # print(description)

    # 2)    Get input from config file
    try:
        soup = retrieve_web_page(URL_path=config['DEFAULT']['URL'])
        title, description = extract_data(soup)
        print(title)
        print(description)
    except validators.errors.InvalidURLError:
        print("Invalid URL provided, can't make request")

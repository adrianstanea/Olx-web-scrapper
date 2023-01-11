from bs4 import BeautifulSoup
import re
import sys
from time import perf_counter
import csv
import os


def print_data(data: list):
    for price, title, link in data:
        print(f"Price: \t{price}")
        print(f"Title: \t{title}")
        print(f"Link:  \t{link}")
        print('-'*50, end='\n')


def format_olx_query_url(url: str, query: str, pagination="") -> str:
    final_url = url+'/d/oferte/q-' + query.replace(' ', '-') + '/'

    if pagination:
        final_url += '?page=' + str(pagination)

    return final_url


def command_line_parsing():
    try:
        return sys.argv[1] == '-log'
    except IndexError:
        # no command line arguments were passed
        return False


def log_decorator(f):
    def wrapper(args):
        if command_line_parsing():
            start_time = perf_counter()
            result = f(args)
            end_time = perf_counter()
            print(f'Request time: {end_time - start_time:.6f} seconds')
            return result
        return f(args)
    return wrapper


@log_decorator
def extract_data(soup: BeautifulSoup):
    price_paragraphs = soup.find_all('p', attrs={'data-testid': 'ad-price'})
    titles = []
    prices = []
    links = []

    regex = re.compile(
        'folie|adaptor|husa|huse|silicon|display|carcasa|android|copie', re.IGNORECASE)

    for paragraph in price_paragraphs:
        try:
            # exista produse care nu contin descriere corecta si nu sunt filtrare; valoare arbitrara sub care consider ca nu este telefon ci accesorii
            if parse_price_to_float(paragraph.text) < 200:
                # print(int(parse_price(paragraph.text)))
                continue

            text: str = paragraph.previous_sibling.text
            # nu vreau sa includ accesorii ci doar telefoane
            if regex.search(text) is not None or regex.match(paragraph.find_parent('a')['href']) is not None:
                continue

            prices.append(parse_price_to_float(paragraph.text))

            link = paragraph.find_parent('a')['href']
            links.append("olx.ro" + link)

            title = paragraph.previous_sibling.text
            titles.append(title)

        except ValueError as e:
            # exista anunturi care nu au pretul trecut si nu poate fi convertit in valoare numerica,  deci ele nu sunt incluse in lista
            pass

    return prices, titles, links


def parse_price_to_float(price: str) -> float:
    numerics = ''.join(val for val in price if val.isnumeric())

    return float(numerics)


def save_to_file(data: list):
    """
        Create a csv file with the data from the current search, if the file already exists, create a new one with an index

    Args:
        data (list): list of tuples containing the price, title and link of the product to be saved
    """
    index = 0
    headers = ['Price', 'Title', 'Link']

    # create directory to store the files if it does not exist
    if not os.path.isdir('./data'):
        os.mkdir('./data')
        print('Directory created successfully')

    # while loop to search for a file name that does not exist
    while True:
        file_name = f'./data/output{"_"+ str(index) if index else ""}.csv'
        try:
            with open(file_name, 'x', encoding='utf8') as f:
                writter = csv.writer(f)

                writter.writerow(headers)
                for price, title, link in data:
                    writter.writerow([price, title, 'olx.ro'+link])
                print(f'File saved successfully to: {file_name}')
            break
        except FileExistsError as e:
            index += 1
            continue

from bs4 import BeautifulSoup
import re


def format_olx_query_url(url: str, query: str, pagination="") -> str:
    final_url = url+'/d/oferte/q-' + query.replace(' ', '-') + '/'

    if pagination:
        final_url += '?page=' + str(pagination)

    return final_url


def extract_data(soup: BeautifulSoup):
    price_paragraphs = soup.find_all('p', attrs={'data-testid': 'ad-price'})
    titles = []
    prices = []
    links = []

    # regex to match folie or adaptor or husa or carcasa
    regex = re.compile(
        r'folie|adaptor|husa|huse|silicon|display|carcasa', re.IGNORECASE)

    for paragraph in price_paragraphs:
        try:

            text: str = paragraph.previous_sibling.text
            # nu vreau sa includ accesorii ci doar telefoane
            if regex.search(text) is not None or regex.match(paragraph.find_parent('a')['href']) is not None:
                # print(text)
                # print('skipping')
                continue

            prices.append(parse_price(paragraph.text))

            link = paragraph.find_parent('a')['href']
            links.append(link)

            title = paragraph.previous_sibling.text
            titles.append(title)

        except ValueError as e:
            # exista anunturi care nu au pretul trecut; cele de schimb
            pass
            # print(e)

    return prices, titles, links


def parse_price(price: str) -> float:
    numerics = ''.join(val for val in price if val.isnumeric())

    return float(numerics)

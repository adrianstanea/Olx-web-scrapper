import configparser
import validator_collection.validators as validators

from WebScrapper import WebScrapper
import utilities

# configuration settings from .ini file
config = configparser.ConfigParser()
config.read('config.ini')

url = config['DEFAULT']['URL']
keywords = config['DEFAULT']['KEYWORDS']
pages = config['DEFAULT']['PAGES']


olx_url = utilities.format_olx_query_url(url, keywords)

if __name__ == '__main__':
    try:
        web_scrapper = WebScrapper(
            url=olx_url)
        soup = web_scrapper.scrape()

        prices, titles, links = utilities.extract_data(soup)

        # read data from the next pages
        for i in range(2, int(pages) + 1):
            web_scrapper.set_url(
                utilities.format_olx_query_url(url, keywords, i))
            soup = web_scrapper.scrape()
            new_prices, new_titles, new_links = utilities.extract_data(soup)
            # extend the lists with the iterables given as arguments
            prices.extend(new_prices)
            titles.extend(new_titles)
            links.extend(new_links)

        data = zip(prices, titles, links)
        data = sorted(data, key=lambda x: x[0])  # descending order by price

        for price, title, link in data:
            print(f'{price} {title} \t{ "olx.ro"+ link}')
            print('---------------------------------')

    except validators.errors.InvalidURLError as e:
        print(e)

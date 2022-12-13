# Web Scraping

_The project is still work-in-progress_

Install dependencies using:

```console
    python -m pip install -r requirements.txt
```

## Current fuctionality

-  The user can provide an URL for a target web page changing the variable from the congig.ini file
-  The script App.js uses the URL and makes an HTTP GET request to the server using [requests library](https://pypi.org/project/requests/)
-  The response is then parsed into an object for easier acces to the data contained within the HTML using [Beautiful Soup ](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup)
-  Finally, after running some validations the title and description are extracted and presented to the user

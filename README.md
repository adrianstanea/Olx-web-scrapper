# Web Scraping

Install dependencies using:

```console
    python -m pip install -r requirements.txt
```

## Current fuctionality

-  The user can run the application with the optional -log flag

```console
    python App.py -log
```

![](/images/Running_script.PNG)

This will extract data from the desired URL and print the result to the console. When -log flag is active the search result is stored under the ./data folder

![](/images/csv_data.PNG)

-  If we find a product under the imposed price limit we notify the user by sending an email with the product data

![](/images/email_results.jpg)

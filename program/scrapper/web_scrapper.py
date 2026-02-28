import requests 
from bs4 import BeautifulSoup
import logging
import time

#web scrappers for the pages used, for now i'll do it like one specific scrapper per page
#initializing logger for the module
logger = logging.getLogger(__name__)

def newegg_scrapper(total_pages: int = 20):
    page_limit = min(total_pages, 20)
    data = []
    pages_failed = 0

    for page_number in range(1, page_limit + 1):
        url = f'https://www.newegg.com/p/pl?d=ram&page={page_number}'
        #validation of the request
        try: 
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f'Failure to connect to URL {url}') from e
        #this if proccess the raw html into raw data
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            web_data = soup.find_all(class_ = 'item-cell')
            for i in web_data:
                price_tag = i.find(class_='price-current')
                description_tag = i.find(class_='item-title')
                if description_tag == None or price_tag == None: 
                    logger.warning('This iteration of listing on newegg does not have price and/or description')
                    continue
                price = price_tag.get_text(strip=True)
                description = description_tag.get_text(strip=True)
                store = {
                    'description': description,
                    'price': price,
                    'source': 'Newegg'}
                data.append(store)
        else:
            logger.warning(f'Page {page_number} failed with status code {response.status_code}, Pages failed: {pages_failed}')
            pages_failed += 1 #this is so if one page fails it doesn't crash the entire scrapper
            if pages_failed == 5:
                raise ConnectionError(f'Failed to retrieve data from URL, too many pages have failed to connect')
            continue
        
        time.sleep(1)

    return data

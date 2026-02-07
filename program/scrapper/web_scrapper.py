import requests 
from bs4 import BeautifulSoup
import logging

#web scrappers for the pages used, for now i'll do it like one specific scrapper per page
#initializing logger for the module
logger = logging.getLogger(__name__)

def newegg_scrapper():
    url = 'https://www.newegg.com/p/pl?d=ram'
    #validation of the request
    try: 
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f'Failure to connect to URL {url}') from e
    #this if proccess the raw html into raw data
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        web_data = soup.find_all(class_ = 'item-cell')
        data = []
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
                'price': price}
            data.append(store)
    else:
        raise ConnectionError(f'Unable to retrieve data, code: {response.status_code}')
    return data
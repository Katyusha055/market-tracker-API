import requests 
from bs4 import BeautifulSoup

url = 'https://www.newegg.com/p/pl?d=ram'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

test = soup.find(class_ = 'item-cell')

title_tag = test.find(class_ = "item-title")
title = title_tag.get_text(strip=True)
print(f'{title} \n')

price_tag = test.find('li', class_='price-current')
price = price_tag.get_text(strip=True)
print(price)
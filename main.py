#!/usr/bin/env python3

import requests 
from bs4 import BeautifulSoup

URL = f"https://wisetekstore.com/collections/refurbished-laptops?page=1&sort_by=price-ascending"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
r = requests.get(url=URL, headers=headers) 
soup = BeautifulSoup(r.content, 'html5lib')

results = soup.find('div', attrs = {'id':'filter-results'}) 
pages = results.find_all('ul', attrs = {'class':'pagination relative flex flex-wrap justify-center items-center justify-between w-full mx-auto mb-10 js-pagination'})
pages = pages[0].find_all('li', attrs = {'class':'pagination__item text-center md:hidden font-bold'})

items = []   
prices = []
page_num = int(pages[0].text.strip().split('/')[1].strip())
for i in range(1, page_num + 1):
  URL = f"https://wisetekstore.com/collections/refurbished-laptops?page={str(i)}&sort_by=price-ascending"
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
  r = requests.get(url=URL, headers=headers) 
  soup = BeautifulSoup(r.content, 'html5lib')
  results = soup.find('div', attrs = {'id':'filter-results'}) 
  price_data = results.find_all('div', attrs = {'class':'price__default'})
  for item in price_data:
    item2 = item.text.strip()
    for c in item2:
      if c.isnumeric() == False and c != ',':
        item2 = item2.replace(c, '')
      elif c == ',':
        item2 = item2.replace(c, '.')
    prices.append(float(item2))
  laptop_text = results.find_all('a')
  for item in laptop_text:
    if item.text.strip() != '' and len(item.text.strip()) > 4:
      items.append(item.text.strip())
  for item in items:
    if item == 'View details':
      items.remove(item)
    if item == 'Previous':
      items.remove(item)
    if item == 'Next':
      items.remove(item)
    if item.isnumeric() == True:
      items.remove(item)

with open('laptops.txt', 'w') as f:
  for item in items:
    try:
      print(f'Laptop: {item}\nPrice: €{prices[items.index(item)]:.2f}')
      f.write(f'Laptop: {item}\nPrice: €{prices[items.index(item)]:.2f}\n\n')
    except IndexError:
      break
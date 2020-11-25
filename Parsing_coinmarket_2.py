# 30.08.2020 Парсинг coinmarket с учетом пагинации сайта.

import requests
from bs4 import BeautifulSoup
import csv
import re


def get_html(url):
	r = requests.get(url)
	if r.ok:
		return r.text
	print(r.status_code)


def refined(s):
	r = s.split('$')[1].strip()
	return r.replace(',', ' ')


def write_csv(data):
	with open('coinmarketcap_basedata.csv', 'a') as f_obj:
		writer = csv.writer(f_obj)
		
		writer.writerow([data['Name'],
						data['Market cap'],
						data['Price'],
						data['URL']])


def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	table = soup.find('div', class_='cmc-table--sort-by__rank').find_all(class_='cmc-table__table-wrapper-outer')[2]
	tables = table.find('tbody').find_all('tr')
	tables.pop(10)

	for tb in tables:
		try:
			name = tb.find('div', class_='cmc-table__column-name').find('a').text
		except:
			name = 'None'
		try:
			url = 'https://coinmarketcap.com' + tb.find('div', class_='cmc-table__column-name').find('a').get('href')
		except:
			url = 'None'
		try:
			market_caps = tb.find('td', class_='cmc-table__cell--sort-by__market-cap').find('p').text
			market_cap = refined(market_caps)
		except:
			market_cap = 'None'
		try:
			prices = tb.find('td', class_='cmc-table__cell--sort-by__price').find('a').text
			price = refined(prices)
		except:
			price = 'None'

		data = {'Name': name,
				'Market cap': market_cap,
				'Price': price,
				'URL': url}

		write_csv(data)
		
		# print(name)
		# print(url)
		# print(market_cap)
		# print(price)
	# print(len(table))


def main():
	url = 'https://coinmarketcap.com/ru/'

	# get_total_pages(get_html(url))

	while True:
		get_total_pages(get_html(url))  # Цикл для перебора страниц

		soup = BeautifulSoup(get_html(url), 'lxml')
		try:
			pattern = 'Следующий'
			url = 'https://coinmarketcap.com' + soup.find('div', class_='cmc-table-listing__pagination-button-group').find('a', text=re.compile(pattern)).get('href')
		except:
			break



if __name__ == '__main__':
	main()
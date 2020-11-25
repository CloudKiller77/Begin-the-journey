# 29.08.2020 Парсинг Coinmarket (табличные данные)

import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
	r = requests.get(url)
	return r.text


def write_csv(data):
	with open('coinmarket.csv', 'a') as f_obj:
		writer = csv.writer(f_obj)
		
		writer.writerow([data['Name'],
						data['Market capital'],
						data['Price'],
						data['URL']])

def refined(s):
	r = s.replace(',', ' ')
	return r


def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	tables = soup.find('div', class_='cmc-table--sort-by__rank').find_all(class_='cmc-table__table-wrapper-outer')[2]
	trs = tables.find('tbody').find_all('tr')
	trs.pop(10)
	url_local = "https://coinmarketcap.com"

	for tr in trs:
		tds = tr.find_all('td')
		name = tds[1].find('div').find('a').text
		url1 = tds[1].find('div').find('a').get('href')
		url = url_local + url1
		market_capitalization = tds[2].find('p').text
		market_capital = refined(market_capitalization)
		prices = tds[3].find('a').text
		price = refined(prices)
		
		data = {'Name': name,
				'Market capital': market_capital,
				'Price': price,
				'URL': url}

		write_csv(data)

	# trs.pop(10)
	# print(len(trs))


def main():
	url = "https://coinmarketcap.com/ru/"
	get_page_data(get_html(url))



if __name__ == '__main__':
	main()
# 30.08.2020 Работа с пагинацией сайта 
# Парсинг яндекс-маркета

import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
	r = requests.get(url)
	if r.ok:
		return r.text
	
	print(r.status_code)


def write_csv(data):
	with open('yandex igrovie noutbuki.csv', 'a') as f_obj:
		writer = csv.writer(f_obj)
		
		writer.writerow([data['Name'],
						data['URL'],
						data['Rating'],
						data['Processor'],
						data['OZU'],
						data['HDD'],
						data['Video'],
						data['Video memory']])


def list_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	lis = soup.find_all('article', class_='cia-cs')
	# print(len(lis))
	for li in lis:
		try:
			name = li.find('span').text
		except:
			name = 'None'
		try:
			url = 'https://market.yandex.ru' + li.find('a').get('href')
		except:
			url = 'None'
		try:
			rating = li.find('a', class_='NF4jhNTZj').find('div', class_='_3sAuwdoAG1').find('div', class_='_3tPFJYQO2f').find('span').text
		except:
			rating = 'None'
		try:
			descriptions = li.find('div', class_='_1oWY5nAvx-').find('ul', class_='_1leWQd9vBF').find_all('li')
			try:
				processor = description[0].text.strip()
			except:
				processor = 'None'
			try:
				ozu = description[1].text.strip()
			except:
				ozu = 'None'
			try:
				hdd = description[2].text.strip()
			except:
				hdd = 'None'
			try:
				video = description[3].text.strip()
			except:
				video = 'None'
			try:
				video_memory = description[4].text.strip()
			except:
				video_memory = 'None'
		except:
			description = 'None'

		# for descript in descriptions:
		# 	processor = descript.text
		data = {'Name': name,
				'URL': url,
				'Rating': rating,
				'Processor': processor,
				'OZU': ozu,
				'HDD': hdd,
				'Video': video,
				'Video memory': video_memory}

		write_csv(data)

				# ozu = descript.text
				# hdd = descript.text
				# video = descript.text
				# video_memory = descript.text
def main():
	pattern = 'https://market.yandex.ru/catalog--igrovye-noutbuki-v-saratove/17635483/list?hid=91013&glfilter=5085102%3A16880592&onstock=1&page={}'
	
	for i in range(1, 15):
		url = pattern.format(str(i))
		list_pages(get_html(url))



if __name__ == '__main__':
	main()
import argparse
import sys
import requests
import locale
from bs4 import BeautifulSoup


class Ccg_obsession:

	def __init__(self):
		self.url = 'http://www.ccgobsession.com/search.php'


	def search(self, card_name):
		searchterm = card_name.replace(' ', '+').lower()
		payload = {'product': 'MG', 'searchterm': searchterm }

		req = requests.post(self.url, data=payload)
		soup = BeautifulSoup(req.text, 'html.parser')
		splitsoup = soup.prettify().splitlines()

		items = []
		stock = True
		for i,v in enumerate(splitsoup):
			if card_name.lower() in v.lower() and 'type="hidden"' in v:
				for c in splitsoup[i:i+8]:
					if 'Out' in c:
						stock = False
				if stock == True:
					items.append(v)
			# reset the stock checker
			stock = True

		stock_list = []
		for i in items:
			stock_list.append(i.split('|')[1:3])


		cheapest = {'name': '', 'price': 0}
		if stock_list:
			for v in stock_list:
				if float(v[1]) < cheapest['price'] or cheapest['price'] == 0:
					cheapest['price'] = float(v[1])
					cheapest['name'] = v[0]
			return cheapest
		else:
			return False


	def format_price(self, price):
		locale.setlocale( locale.LC_ALL, '' )
		return locale.currency(price)
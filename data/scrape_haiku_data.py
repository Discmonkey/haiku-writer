import os
import json
import urllib2
from bs4 import BeautifulSoup

import argparse

BASE_URL = 'http://www.tempslibres.org/tl/tlphp/{}'
URL = BASE_URL.format('dbauteursl.php?lang=en&lg=e')


parser = argparse.ArgumentParser()

parser.add_argument('output_file')
parser.add_argument('-l', '--limit',
					type=int,
					help='Limits how many haikus are collected. Leave blank to collect all ' +
					'that can be found')

args = parser.parse_args()

page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

def format_haiku(haiku):
	haiku_text = haiku.replace('\r', '').split('\n\n')[0]
	haiku_lines = [elm.strip() for elm in haiku_text.split('\n')]

	return haiku_lines

def get_haiku(haiku_elm):
	haiku = haiku_elm.text
	return format_haiku(haiku)

def get_haikus(link):
	haiku_page = urllib2.urlopen(link)
	haiku_soup = BeautifulSoup(haiku_page, 'html.parser')

	content = haiku_soup.find('article', {'id': 'content'})
	author = content.find('h2').text.strip()
	haiku_elms = content.find_all('p', {'class': 'haiku'})

	haikus = []
	for haiku_elm in haiku_elms:
		haiku = get_haiku(haiku_elm)
		haikus.append(haiku)

	ret_data = {
		author: {
			"url": link,
			"haikus": haikus
		}
	}
	return author, haikus

table = soup.find('table')
table_rows = table.find_all('a', href=True)
links = [row['href'] for row in table_rows]

stop = False
count = 0
collected_haikus = {}
for link in links:
	haiku_page_link = BASE_URL.format(link)
	print haiku_page_link

	author, haikus = get_haikus(haiku_page_link)
	if args.limit and len(haikus) >= args.limit:
		haikus = haikus[:args.limit]
		stop = True

	count += len(haikus)
	collected_haikus.setdefault(author, {
			"url": link,
			"haikus": haikus
		})

	if stop:
		break

print 'Collected {} haiku(s)!'.format(count)

with open(args.output_file, 'w') as f:
	json.dump(collected_haikus, f, indent=4)

print 'Done. Data written to {}'.format(args.output_file)

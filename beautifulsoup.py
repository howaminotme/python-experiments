#!/usr/bin/env python

import time
import requests
import bs4
import random
import re
from optparse import OptionParser
import datetime
import collections

parser = OptionParser()
parser.add_option('-t', '--time', type='string', action='store', dest='time', help='Time in seconds for the crawler to sleep in between cycles')
(opts, args) = parser.parse_args()
sleep_cycle = float(opts.time)


initial_link = ['http://blog.readyforzero.com/']
set_of_links = set(initial_link)
external_links = collections.defaultdict(set)

def crawler():
	page = random.sample(set_of_links, 1)[0]
	print "\n\nCrawling to %s and collecting its links" % (page)

	try:
		target_page = (requests.get(page, headers={'User-agent': 'Python_Spider'})).text
		soup = bs4.BeautifulSoup(target_page)
	except:
		pass

	for link in soup.find_all('a'):
		try:
			if re.match("^http://blog.readyforzero.com", link.get('href')):
				set_of_links.add(link.get('href'))

			else:
				external_links[(link.get('href'))].add(page)
		except:
			pass


def page_checker(x):
	now = datetime.datetime.now()
	page = random.sample(x,1)[0]
	print "\n\nChecking returned status code on " + page

	try:
		target_page = (requests.get(page, headers={'User-agent': 'Python_Spider'}))
	except:
		pass

	external_logs = open('external_status_codes', 'a')
	local_logs = open('blog_status_codes', 'a')
	
	try:
		if re.match("^http://blog.readyforzero.com", page):
			if target_page.status_code != 200:
				local_logs.write(str(page) + ' ' + str(target_page.status_code) + ' ' + str(now) + '\n')
			else:
				pass

		else:
			if target_page.status_code != 200:
				thing = (str(page) + ' ' + str(target_page.status_code) + ' ' + str(now) + ' ' + str(external_links[page]) + '\n')
				external_logs.write(thing)
			else:
				pass

	except:
		pass

	external_logs.close()
	local_logs.close()


while True:
	print "\n\n--------------------STARTING NEW CYCLE--------------------\n\n"
	print "Current collection of links contains %s entries\n\n" % (len(set_of_links))
	print "External links collected " + str(len(external_links))
	crawler()
	page_checker(set_of_links)
	page_checker(external_links)
	time.sleep(sleep_cycle)

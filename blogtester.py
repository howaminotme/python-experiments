#!/usr/bin/env python

import requests
import datetime
import time

watch_list = [
	'http://blog.readyforzero.com/page/2/',
	'http://blog.readyforzero.com/page/5/',
	'http://blog.readyforzero.com/resources/get-out-of-debt/',
	'http://blog.readyforzero.com/category/success-profiles'
	]



page2_len_master = 0
page5_len_master = 0
goodrc_len_master = 0
sp_len_master = 0


page2_file = open('page2_returns.txt','a')
page5_file = open('page5_returns.txt','a')
goodrc_file = open('goodrc_returs.txt','a')
sp_file = open('sp_returns.txt','a')


first_loop = 1

while True:
	page2 = requests.get(watch_list[0])
	page5 = requests.get(watch_list[1])
	goodrc = requests.get(watch_list[2])
	sp = requests.get(watch_list[3])

	now = datetime.datetime.now()

	if first_loop == 1:
		page2_len_master = len(page2.text)
		page5_len_master = len(page5.text)
		goodrc_len_master = len(goodrc.text)
		sp_len_master = len(sp.text)

		first_loop = 2

		
	
	page2_file.write('\n'+str([now, page2.status_code, (page2_len_master / len(page2.text)), page2.text.replace('\n','')]))
	
	page5_file.write('\n'+str([now, page5.status_code, (page5_len_master / len(page5.text)), page5.text.replace('\n','')]))
	
	goodrc_file.write('\n'+str([now, goodrc.status_code, (goodrc_len_master / len(goodrc.text)), goodrc.text.replace('\n','')]))

	sp_file.write('\n'+str([now, sp.status_code, (sp_len_master / len(sp.text)), sp.text.replace('\n','')]))

	time.sleep(60)

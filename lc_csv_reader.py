#!/usr/bin/env python

import csv
from optparse import OptionParser
import matplotlib.pyplot as pyplot
import collections
from datetime import date, timedelta as tdelta
import numpy as np

parser = OptionParser()
parser.add_option("-f", type="string", action='store', dest='file', help='Target a specific csv file for analysis.')
(opts, args) = parser.parse_args()

file = opts.file


class lc_loan:
	'Common base class for all LC loans'
	def __init__(self,leadId,RefID,Param2,ActorId,App_Date,
			Offer_Date,Expire_Date,ListedDate,Issued_Date,
			Requested_Amt,Listed_Amt,Issued_Amt,App_Status,
			Final_Status,Term,Purpose,Product):
		
		self.leadId = leadId
		self.RefID = RefID
		self.Param2 = Param2
		self.ActorId = ActorId
		self.App_Date = App_Date
		self.Offer_Date = Offer_Date
		self.Expire_Date = Expire_Date
		self.ListedDate = ListedDate
		self.Issued_Date = Issued_Date
		self.Requested_Amt = Requested_Amt
		self.Listed_Amt = Listed_Amt
		self.Issued_Amt = Issued_Amt
		self.App_Status = App_Status
		self.Final_Status = Final_Status
		self.Term = Term
		self.Purpose = Purpose
		self.Product = Product


master_list = []

lc_object_list = []

def read_print(x):
        reader = csv.reader(x)
        for row in reader:
                master_list.append(row)

def transform(x):
	for i in x:
		lc_object_list.append(lc_loan(*i))


target = open(file)

read_print(target)

make_it_so = transform(master_list[3:])

#funciton to grab / sort by date

def date_grabber(x):
	app_dates = []
	for i in x:
		 app_dates.append(i.App_Date[:10])
	date_counter = collections.Counter(app_dates)
	ordered = collections.OrderedDict(sorted(date_counter.items(), key=lambda t: t[0]))
	formatted_dates = {(str(key[6:10])+'-'+str(key[0:2])+'-'+str(key[3:5])): value for (key, value) in date_counter.iteritems()}
	return (ordered,formatted_dates)

#function to grab / Listed date

def listed_grabber(x):
	listed_dates = []
	listed_dates_junk = []
	for i in x:
		if i.ListedDate != '-':
			listed_dates.append(i.ListedDate[:10])
		else:
			listed_dates_junk.append(i)
	listed_counter = collections.Counter(filter(lambda i: i != '-', listed_dates))
	ordered = collections.OrderedDict(sorted(listed_counter.items(), key=lambda t: t[0]))
	formatted_dates = {(str(key[6:10])+'-'+str(key[0:2])+'-'+str(key[3:5])): value for (key, value) in listed_counter.iteritems()}
	return (ordered,formatted_dates)

#function to grab / issued amount by date

def issued_grabber(x):
	issued_info = collections.defaultdict(list)
	for i in x:
		issued_info[i.App_Date[:10]].append(float(i.Issued_Amt))
	formatted_dates = {(str(key[6:10])+'-'+str(key[0:2])+'-'+str(key[3:5])): sum(value) for (key, value) in issued_info.iteritems()}
	return formatted_dates


#fucntion to pull apart a ditionary for easy graphing with pyplot

def dict_unfucker(x):
	keys = []
	values = [0]
	for key, value in x.iteritems():
		keys.append(key)
		values.append(value)
	return (keys,values)


def moving_average(x):
	weigths = np.repeat(1.0, 30) / 30
	#including valid will REQUIRE there to be enough datapoints.
	#for example, if you take out valid, it will start @ point one,
	#not having any prior points, so itll be 1+0+0 = 1 /3 = .3333
	ma = np.convolve(x, weigths, 'valid')
	format_ma = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	#format_ma = [0,0,0,0,0,0]
	for i in ma:
		format_ma.append(int(round(i)))
	return format_ma # as a numpy array


#Establish base time metric in the form of a dict

d1 = (dict_unfucker(date_grabber(lc_object_list)[0])[0])[0]
d2 = (dict_unfucker(date_grabber(lc_object_list)[0])[0])[-1]
delta2 = date(int(d2[6:10]),int(d2[0:2]),int(d2[3:5]))
delta1 = date(int(d1[6:10]),int(d1[0:2]),int(d1[3:5]))

delta = delta2 - delta1

master_time = {}

for i in range(delta.days + 1):
    master_time[str(delta1 + tdelta(days=i))] = 1

#map the LC applicationdate data to the master time metric

time = collections.Counter(master_time)
application_date = collections.Counter(date_grabber(lc_object_list)[1])
listed_date = collections.Counter(listed_grabber(lc_object_list)[1])
issued_date = collections.Counter(issued_grabber(lc_object_list))

ordered_app_by_date_tally = collections.OrderedDict(sorted((time+application_date).items(), key=lambda t: t[0]))
ordered_listed_date_tally = collections.OrderedDict(sorted((time+listed_date).items(), key=lambda t: t[0]))
ordered_issued_date_tally = collections.OrderedDict(sorted((time+issued_date).items(), key=lambda t: t[0]))


pyplot.figure(figsize=(12,6), dpi = 600)
pyplot.axis([0.0 ,(5 + len(master_time)), 0.0, (max(dict_unfucker(ordered_app_by_date_tally)[1]))])
pyplot.axis([0.0 ,(5 + len(master_time)), 0.0, 100.0])
pyplot.xlabel('Days: ' + (str((dict_unfucker(ordered_app_by_date_tally)[0])[0])) + ' through ' + (str((dict_unfucker(ordered_app_by_date_tally)[0])[-1])) + '\n (Values aligned to App date)')
pyplot.ylabel('Total Amount')
pyplot.xticks((range(0,1+len(master_time))[::30]))

pyplot.plot((range(1+len(dict_unfucker(ordered_app_by_date_tally)[0]))), (dict_unfucker(ordered_app_by_date_tally)[1]), color = 'b', label = 'Loan Apps')

pyplot.plot((range(1+len(dict_unfucker(ordered_app_by_date_tally)[0]))), (moving_average(dict_unfucker(ordered_app_by_date_tally)[1])), color = 'r', label = "Loan Apps - 30day SMA")

pyplot.plot((range(1+len(dict_unfucker(ordered_listed_date_tally)[0]))), (dict_unfucker(ordered_listed_date_tally)[1]), color = 'g', label = 'Listed loans')

pyplot.plot((range(1+len(dict_unfucker(ordered_listed_date_tally)[0]))), moving_average([0]+[(100*x/y) for (x,y) in zip((dict_unfucker(ordered_listed_date_tally)[1]), (dict_unfucker(ordered_app_by_date_tally)[1])) if y != 0]), color = 'm', label = """Listed vrs App'd %- 30day SMA""")

#pyplot.bar((range(1+len(dict_unfucker(ordered_issued_date_tally)[0]))), (dict_unfucker(ordered_issued_date_tally)[1]), color = 'g', label = 'Issued Amount')

#pyplot.plot((range(1+len(dict_unfucker(ordered_issued_date_tally)[0]))), (moving_average(dict_unfucker(ordered_issued_date_tally)[1])), color = 'r', label = "Issued Amount - 30 day SMA")

#print [(100 * x/y) for (x,y) in zip((dict_unfucker(ordered_listed_date_tally)[1]), (dict_unfucker(ordered_app_by_date_tally)[1])) if y !=0 ]

pyplot.legend(loc='upper left')
pyplot.savefig('LC-Issued-V-Listed.png')

print """\n\n*Please check your present working directory for a '.png' to review the graph\n\n"""


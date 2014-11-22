#!/usr/bin/env python

import csv
from optparse import OptionParser
import matplotlib.pyplot as pyplot
 
parser = OptionParser()
parser.add_option("-f", type="string", action='store', dest='file', help='Target a specific csv file for analysis.')
parser.add_option("-p", type="string", action='append', dest='previous', help='Compare your target to a previous csv file. Files should be added in sequential order extending back in time')
(opts, args) = parser.parse_args()

file = opts.file
previous = opts.previous

master_list = []
current_status = []
issue_date = []
tally_for_delta = [0.0]

def read_print(x):
	reader = csv.reader(x)
	for row in reader:
		master_list.append(row)

target = open(file)

read_print(target)


def loan_status_grabber(x):
	for i in x[3:]:
		try:
			current_status.append(i[12])
			issue_date.append(i[8])
		except:
			print "weird line in csv file - likely a header or lable"


loan_status_grabber(master_list)

def tally_of_status(x):
	Applied = 0
	Duplicate = 0
	Listed = 0
	Offered = 0
	total = len(x)
	for i in x:
		if i == 'Applied':
			Applied += 1
		elif i == 'Duplicate':
			Duplicate += 1
		elif i == 'Listed':
			Listed += 1
		elif i == 'Offered':
			Offered += 1
		else:
			print i

	

	print """\n--------------------The break down of loan states is as follows:-------------------- \n 
	Applied: %s (%s percent) \n 
	Duplicate: %s (%s percent) \n
	Listed: %s (%s percent) \n 
	Offered: %s (%s percent) \n 
	Out of a total of: %s loans""" % (Applied, (int(float(Applied) / float(total) * 100)) ,
						 Duplicate, (int(float(Duplicate) / float(total) * 100)),
						 Listed, (int(float(Listed) / float(total) * 100)),
						 Offered, (int(float(Offered) / float(total) * 100)),
						 total)
	print "\n*Note that percentages are rounded off, and therefore may not add to 100%"



def tally_of_issued(x):
	closed = 0
	unknown	= 0
	total = len(x)
	for i in x:
		if i == '-':
			unknown += 1
		else:
			closed += 1

	tally_for_delta.append(round(100 * (float(closed) / float(total)),2))	

	print """\nThe breakdown of Closed vrs Open loans is as follows:\n
	%s closed loans and %s in a open status \n 
	This represents a %s percent close rate out of %s total \n""" % (closed, unknown, round(100 * (float(closed) / float(total)),2),total)


tally_of_status(current_status) 
tally_of_issued(issue_date)


def one_more_time(x):
	master_list[:] = []
	current_status[:] = []
	issue_date[:] = []

	
	print "--------------------------Information for the prior month:--------------------------"
	target = open(x)
	read_print(target)
	loan_status_grabber(master_list)
	tally_of_status(current_status)
	tally_of_issued(issue_date)


if previous:
	for i in previous:
		one_more_time(i)

else:
	print "*No prior months to compare to.\n"

metric = [x * 1.0 for x in range(0, len(tally_for_delta))]


if previous:
	pyplot.axis([0.0 ,(1 + len(tally_for_delta)), 0.0, (1 + max(tally_for_delta))])
	pyplot.xticks(metric) 
	pyplot.xlabel('Months')
	pyplot.ylabel('Loan Completion rate in Percent')
	pyplot.plot(metric,tally_for_delta)
	pyplot.savefig('delta.png')
	print """\n\n*Please check your present working directory for a 'delta.png' to review the graph\n\n"""

else:
	print "*No Graph generated"

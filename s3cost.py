#!/usr/bin/env python

import boto
import boto.s3.connection
import boto.s3.key
from optparse import OptionParser


#options for target bucket - and verbose cost analysis 
parser = OptionParser()
parser.add_option("-b", type="string", action='store', dest='bucket', help='Target a specific bucket for analysis. Format should be an all lower case string')
parser.add_option("-v", action="store_true", dest="verb", default=False, help="Print individual cost breakdown of all items in target bucket")
(opts, args) = parser.parse_args()
target = opts.bucket
verbose = opts.verb

#AWS creds for S3 user 
awsid = ''
secid = ''
sizes = {}
costs = {}

#aws connection objects 
conn = boto.s3.connection.S3Connection(awsid,secid)
bucket = conn.get_bucket(target)
keys = bucket.list()

ac = 0

#iterate though bucket keys and append to local dict
for key in keys:
	sizes[key.name] = key.size
	ac += 1
	if ac % 1000 == 0:
		print "Pulling key %s" % (ac)

#iterate though bucket dict and calculate cost for each key
for i in sizes:
	costs[i] = (sizes[i] * (0.08/1024**3))

#calculate total storage size and cost
totalsize = (sum(sizes.itervalues()))/1024**3
totalcost = round(sum(costs.itervalues()))


#print analysis to console
if verbose == False:
	print "%s as a whole is %s GB, and costs aproximately $%s per month" % (target,totalsize,totalcost)

else:
	print "%s as a whole is %s GB, and costs us aproximately $%s per month, here is the breakdown per item in dollars:" % (target,totalsize,totalcost)  
	for key, value in costs.iteritems():
    		print key, value


#!/usr/bin/env python

#script for monitoring disk and partition usage

import subprocess
from optparse import OptionParser
import httplib

# allow script to accept options - specifically partitions to ignore

parser = OptionParser()
parser.add_option('-i', '--ignore', type='string', action='append', dest='ignore')
(opts, args) = parser.parse_args()
ignore = opts.ignore

# pass df to shell and capture output
df = subprocess.Popen(["df"], stdout=subprocess.PIPE)
output = df.communicate()[0]
disklist = output.split("\n")

fillrates = {}

# evaluate df output and extract the partition + fill rate 
for lines in disklist[1:-1]:
    part = lines.split()    
    usage_int = int(part[4].replace("%",""))
    if usage_int > 0:
        fillrates[part[0]] = usage_int

# pull out partitians that are to be ignored

if len(ignore) > 0:
    print "Ignoring partitians %s" % (ignore)
    for i in ignore:
        del fillrates[i]
else:
    print "No partitians ignored"

# of the remaining parititans target the file system that is most full
dangerzone = max(fillrates, key=fillrates.get)
    
print "The File system on %s is currently %s percent full" % (dangerzone, fillrates[dangerzone])


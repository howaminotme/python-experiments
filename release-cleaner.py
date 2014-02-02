#!/usr/bin/env python

import time
import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-t', '--target', type='string', action='append', dest='target', help='Directories to be cleaned, with base number of files to be kept and file expressions to ignore, Format : /home/ec2-user/debtapp/current:10:gz')
(opts, args) = parser.parse_args()

target = opts.target

def clean(x):
	#break apart target info
	bits = x.split(":")
	dir = bits[0]
	max_objects = int(bits[1])
	ignore_objects = bits[2]

	#Count non ignored files in target dir and store the count for evaluation 
	look_for_stuff = subprocess.Popen(["ls -tr %s | grep -v %s | wc -l" % (dir,ignore_objects)], shell=True, stdout=subprocess.PIPE)
	count = int(look_for_stuff.communicate()[0])

	#evaluate war count, take action if count exceeds threshold
	excess = (count - max_objects)
	prun_files = subprocess.call(["cd %s ; ls -tr %s | grep -v %s | head -%s | xargs rm" % (dir,dir,ignore_objects,excess)], shell=True)


#call clean on all targets passed to script

while True:

	for i in target:
		clean(i)


	time.sleep(3600)

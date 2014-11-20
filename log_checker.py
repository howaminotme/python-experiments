#!/usr/bin/env python
import time
import datetime
import boto.ses
import subprocess

Access_Key_ID = 
Secret_Access_Key = 

while True:
	current = datetime.datetime.now()
	day = current.weekday()
	hour = current.hour
	strtime = str(current)

	logcheck = subprocess.Popen(["""grep "200 5 " /var/log/nginx/access.log"""], stdout=subprocess.PIPE , shell=True)
	output = logcheck.communicate()[0]
	loglist = output.split("\n")

	def send_summary_email():
        	SESconnect = boto.ses.connection.SESConnection(Access_Key_ID, Secret_Access_Key)
        	body_of_email = "A review of the nginx access logs for the prior day has revealed %s instances of blank pages being served. Please review them" % (len(loglist))
        	Subject ='Blog Blank Page Alert'
        	SESconnect.send_email(
                	'engineering@readyforzero.com',
               		Subject,
                	body_of_email,
                	'engineering@readyforzero.com',
                	format='text')


	if hour == 22:
		send_summary_email(latency, counts)


	time.sleep(3600)


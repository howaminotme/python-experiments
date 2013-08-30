#!/usr/bin/env python

#scrpit for monitoring disk usage on the blog machine

import subprocess
from smtplib import SMTP

#check status of disk / partition with "df" command. Evaluate return.

df = subprocess.Popen(["df", "/dev/sda1"], stdout=subprocess.PIPE)

output = df.communicate()[0]

device, size, used, available, percent, mountpoint = \
    output.split("\n")[1].split()


print "The partition mounted on /dev/sda1 is %s full" % (percent)

#create variable that is an intiger for easier evaluation
usage_int = int(percent.replace("%", ""))


#funciton for taking action once threshold is reached - goal is to email someone if disk usage exceeds 80%
if usage_int > 0:

    sender = "help@readyforzero.com"
    recievers = "bobby@readyforzero.com"
    subject = "Disk almost full!"
    stupid = """%"""

    message = """From:RFZ Blog Machine %s\r\nTo: Eng %s\r\nSubject: %s\r\n
    This email is a friendly heads up that the disk on the Blog machine is nearly full. It is currently %s%s full.""" % (sender, recievers, subject, usage_int, stupid)

    username = "random@readyforzero.com"
    password = "GETsendgrid123"
    smtp = SMTP()


    print "Sending email to Ben informing him his Blog is about to explode"
    try:
	#smtp.set_debuglevel(True)
        smtp.connect('smtp.sendgrid.net', 587)
        smtp.login(username, password)
        smtp.sendmail(sender, recievers, message)
        print "Successfully sent email"
    except Exception as whut:
        print "Error: unable to send email"
	print whut
    finally:
        smtp.quit()

else:
    print "Disk still has plenty of room!"



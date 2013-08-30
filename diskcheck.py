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
    recievers = ["bobby@readyforzero.com"]

    message = """From: From RFZ Blog Machine <help@readyforzero.com>
    To: bobby <bobby@readyforzero.com>
    Subject: Blog Machine disk usage Warning

    This email is a friendly heads up that the Disk on the Blog machine is nearly full. Tell Ben to stop wiriting so much!
    """

    username = "random@readyforzero.com"
    password = "GETsendgrid123"


    print "sending email to Ben informing him his Blog is about to explode"
    try:
        SMTP.connect('smtp.sendgrid.net', 587)
        SMTP.login(username, password)
        SMTP.sendmail(sender, receivers, message)
        print "Successfully sent email"
    except:
        print "Error: unable to send email"
    finally:
        SMTP.quit()

else:
    print "Disk still has plenty of room!"



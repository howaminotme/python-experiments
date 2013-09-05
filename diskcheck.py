#!/usr/bin/env python

#scrpit for monitoring disk usage on the blog machine

import subprocess
from smtplib import SMTP
#import argparse
from optparse import OptionParser
import time


#allows for arguments to be passed when invoking script - Should use argparser, some code is written with optparse to work on older versions of python.
#for use with 'argparse'
#parser = argparse.ArgumentParser()
#parser.add_argument("path")
#parser.add_argument("threshold")
#opts = parser.parse_args()

#for use with 'optparse'
parser = OptionParser()
parser.add_option("-p", type="string", dest='path')
parser.add_option("-t", type="string", dest='threshold')
(opts, args) = parser.parse_args()


stupid = """%""" #!! stupid?
truth = 1

#insert a loop to check every hour

while truth == 1: #!! can just say 'while True:'

    print "Checking partition mounted at: %s, against a fill threshold of %s%s" % (opts.path, opts.threshold, stupid)


    #check status of disk / partition with "df" command. Evaluate return.

    df = subprocess.Popen(["df", opts.path], stdout=subprocess.PIPE)

    output = df.communicate()[0]

    device, size, used, available, percent, mountpoint = \
        output.split("\n")[1].split()


    print "The partition mounted on %s is %s full" % (opts.path, percent)

    #create variable that is an intiger for easier evaluation
    usage_int = int(percent.replace("%", ""))


    #funciton for taking action once threshold is reached - goal is to email someone if disk usage exceeds the threshold passed
    if usage_int > int(opts.threshold):

        sender = "<help+noreply@readyforzero.com>"
        recievers = "<engineering@readyforzero.com>"
        subject = "Disk almost full!"

        message = """From:RFZ Blog Machine %s\r\nTo: Eng %s\r\nSubject: %s\r\n
        This email is a friendly heads up that the disk on the Blog machine is nearly full. The partition or disk mounted at %s is currently %s%s full.""" % (sender, recievers, subject, opts.path, usage_int, stupid)

        username = "rfzblogmachine"
        password = "diskcheck"
        smtp = SMTP()


        print "Sending email to Ben informing him his Blog is about to explode"
        try:
            #smtp.set_debuglevel(True)
            smtp.connect('smtp.sendgrid.net', 587)
            smtp.starttls()
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


    time.sleep(3600)

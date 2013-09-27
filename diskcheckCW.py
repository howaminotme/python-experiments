#!/usr/bin/env python

#script for monitoring disk and partition usage
import time
import subprocess
from optparse import OptionParser
import boto
import boto.ec2.cloudwatch
import socket

# allow script to accept options - specifically partitions to ignore

parser = OptionParser()
parser.add_option('-i', '--ignore', type='string', action='append', dest='ignore', help='Partitions to be excluded from monitoring')
parser.add_option('-m', '--machine', type='string', action='store', dest='prodstage', help='Prod or Stage designaton, should be either <infrastructure-prod> or <infrastructure-stage>')
(opts, args) = parser.parse_args()
ignore = opts.ignore
prodstage = opts.prodstage

arn = "arn:aws:sns:us-east-1:956924235346:testing-disk-check"
alarmcheck = 0

while True:
    # pass df to shell and capture output
    df = subprocess.Popen(["df"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    disklist = output.split("\n")

    # Gloabal variables
    fillrates = {}
    hostname = socket.gethostname()

    # evaluate df output and extract the partition + fill rate 
    for lines in disklist[1:-1]:
        part = lines.split()    
        usage_int = int(part[4].replace("%",""))
        if usage_int > 0:
            fillrates[part[0]] = usage_int

    # pull out partitions that are to be ignored

    if ignore:
        print "Ignoring partitions %s" % (ignore)
        for i in ignore:
            if i in fillrates:
                del fillrates[i]
    else:
        print "No partitions ignored"

    # of the remaining parititons target the file system that is most full
    dangerzone = max(fillrates, key=fillrates.get)
    
    print "The File system on %s is currently %s percent full" % (dangerzone, fillrates[dangerzone])


    #boto to call cloudwatch and post dangerzone as a metric
    dimes = {'host':hostname, 'partition':dangerzone}

    CWconnect = boto.ec2.cloudwatch.CloudWatchConnection(aws_access_key_id='AKIAI2SSX2FGTWX7TB2Q', aws_secret_access_key='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')

    pushmetric = CWconnect.put_metric_data(namespace=str(prodstage), name='disk-fill', value=fillrates[dangerzone], unit='Percent', dimensions=dimes)

    if alarmcheck == 0:
        alarm = boto.ec2.cloudwatch.alarm.MetricAlarm(
        name='Automated-Diskcheck-alarm',
        metric='disk-fill',
        namespace=str(prodstage),
        statistic='Maximum',
        comparison='>=',
        description='testing alarm',
        threshold=2,
        period=60,
        evaluation_periods=1,
        dimensions=dimes,
        alarm_actions=[arn])
#        ok_actions = [TOPIC],
#        insufficient_data_actions = [TOPIC]

        CWconnect.put_metric_alarm(alarm)

        alarmcheck += 1

    time.sleep(60)

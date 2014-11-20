#!/usr/bin/env python

#script for monitoring partition and inode usage
import time
import subprocess
from optparse import OptionParser
import boto
import boto.ec2.cloudwatch
import socket

# allow script to accept options - specifically partitions to ignore

parser = OptionParser()
parser.add_option('-i', '--ignore', type='string', action='append', dest='ignore', help='Partitions to be excluded from monitoring')
parser.add_option('-m', '--machine', type='string', action='store', dest='prodstage', help='Prod or Stage designaton, should be either <infrastructure-production> or <infrastructure-staging>')
(opts, args) = parser.parse_args()
ignore = opts.ignore
prodstage = opts.prodstage

#gloabal CloudWatch credentials 
arn = "none"
arni = "none"
prodarn = 
prodarni = 
stagearn = 
stagearni = 
alarmfirsttime = True
metname = 'none'
metnamei = 'none'

if prodstage == "infrastructure-production":
    arn = prodarn
    arni = prodarni
    metname = "infrastructure-prod-disk-fill"
    metnamei = "infrastructure-prod-inode-fill"
elif prodstage == "infrastructure-staging":
    arn = stagearn
    arni = stagearni
    metname = "infrastructure-staging-disk-fill"
    metnamei = "infrastruture-staging-inode-fill"
else:
    print "Machine option (-m) not properly set. Should be should be either <infrastructure-production> or <infrastructure-staging>"
    quit()

while True:
    # pass df to shell and capture output
    df = subprocess.Popen(["df"], stdout=subprocess.PIPE , shell=True)
    output = df.communicate()[0]
    disklist = output.split("\n")

    dfi = subprocess.Popen(["df -i"], stdout=subprocess.PIPE , shell=True)
    outputi = dfi.communicate()[0]
    disklisti = outputi.split("\n")

    # Gloabal variables
    fillrates = {}
    fillratesi = {}
    hostname = socket.gethostname()

    # evaluate df output and extract the partition + fill rate 
    for lines in disklist[1:-1]:
        part = lines.split()    
        usage_int = int(part[4].replace("%",""))
        if usage_int > 0:
            fillrates[part[0]] = usage_int

    for lines in disklisti[1:-1]:
        part = lines.split()
        usage_int = int(part[4].replace("%",""))
        if usage_int > 0:
            fillratesi[part[0]] = usage_int

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
    dangerzonei = max(fillratesi, key=fillratesi.get)
    print "The File system on %s is currently %s percent full" % (dangerzone, fillrates[dangerzone])
    print "The inode table on %s is currently %s percent full" % (dangerzonei, fillratesi[dangerzonei])    

    #boto to call cloudwatch and post dangerzone as a metric
    dimes = {'host':hostname, 'partition':dangerzone}

    CWconnect = boto.ec2.cloudwatch.CloudWatchConnection(aws_access_key_id='', aws_secret_access_key='')

    pushmetric = CWconnect.put_metric_data(namespace=str(prodstage), name='disk-fill', value=fillrates[dangerzone], unit='Percent', dimensions=dimes)

    if alarmfirsttime == True:
        alarm = boto.ec2.cloudwatch.alarm.MetricAlarm(
        name= metname + "-" + hostname,
        metric='disk-fill',
        namespace=str(prodstage),
        statistic='Maximum',
        comparison='>=',
        description='A disk partition is over 80% full, or has failed to check in.',
        threshold=80,
        period=3600,
        evaluation_periods=1,
        dimensions=dimes,
        alarm_actions=[arn],
        insufficient_data_actions=[arn])

        CWconnect.put_metric_alarm(alarm)

        alarmfirsttime = False


    if fillratesi[dangerzonei] > 80:
        dimesi = {'host':hostname, 'partition':dangerzonei}

        pushmetric = CWconnect.put_metric_data(namespace=str(prodstage), name='inode-fill', value=fillratesi[dangerzonei], unit='Percent', dimensions=dimesi)

        alarmi = boto.ec2.cloudwatch.alarm.MetricAlarm(
        name= metnamei + "-" + hostname,
        metric='inode-fill',
        namespace=str(prodstage),
        statistic='Maximum',
        comparison='>=',
        description='An inode table is over 80% full.',
        threshold=80,
        period=3600,
        evaluation_periods=1,
        dimensions=dimesi,
        alarm_actions=[arni])

        CWconnect.put_metric_alarm(alarmi)


    time.sleep(3600)

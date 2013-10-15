#!/usr/bin/env python


# scrpt to automatically generate tar.gz backups and push them to s3

import subprocess
from optparse import OptionParser
import boto
import boto.s3.connection
import boto.s3.key
import time
import datetime

keyid = 
seckey = 
current = datetime.datetime.now()
day = current.weekday()
hour = current.hour

#pass options to script

parser = OptionParser()
parser.add_option('-p', '--path', type='string', action='store', dest='tarpath', help='path to directory to be archived. If none set /home/ec2-user will be archived')
parser.add_option('-d', '--destination', type='string', action='store', dest='archdest', help='archive destination path. If none set destination will be /tmpfs')
parser.add_option('-s', '--stack', type='string', action='store',dest='stack', help='prod or stage machine stack. This is to clarify S3 buckets')
parser.add_option('-m', '--machine-type', type='string', action='store',dest='machine', help='machine type <yservice>, <daemons>, <web>.This is to clarify S3 buckets')
(opts, args) = parser.parse_args()
tarpath = opts.tarpath
archdest = opts.archdest
stack = opts.stack
machine = opts.machine


while True:

    current = datetime.datetime.now()
    day = current.weekday()
    hour = current.hour
    strtime = str(current)

    if day == 6 and hour == 2:

        #pass tar to shell to create archive

        backup = subprocess.call(["tar -zcf %s/backup.tar.gz %s" % (archdest,tarpath)], shell=True)

        #push archive to S3

        conn = boto.s3.connection.S3Connection(keyid,seckey)
        new_bucket = conn.create_bucket("rfz-%s-%s-backups" % (stack,machine))
        k = boto.s3.key.Key(new_bucket)
        k.key = strtime.replace(' ','-')
        k.set_contents_from_filename("%s/backup.tar.gz" % (archdest))

        #clean up mess

        print ("cleaning up tar ball mess > rm %s*" % (archdest))
        clean_up = subprocess.call(["rm %s*" % (archdest)], shell=True)

    time.sleep(3600)


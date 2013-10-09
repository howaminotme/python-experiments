#!/usr/bin/env python


# scrpt to automatically generate tar.gz backups and push them to s3

import subprocess
from optparse import OptionParser
import boto
import boto.s3.connection
import boto.s3.key

keyid = 'AKIAIZPOLLFCKHQEDZZQ'
seckey = 'PK+6ZYPMB+ixE+yWl6Op32ljvlpZu5ttQRpw3f4b'


#pass options to script

parser = OptionParser()
parser.add_option('-p', '--path', type='string', action='store', dest='tarpath', help='path to directory to be archived. If none set /home/ec2-user will be archived')
parser.add_option('-d', '--destination', type='string', action='store', dest='archdest', help='archive destination path. If none set destination will be /tmpfs')
(opts, args) = parser.parse_args()
tarpath = opts.tarpath
archdest = opts.archdest


  
#pass tar to shell to create archive

backup = subprocess.call(["tar -zcf %s/backup.tar.gz %s" % (archdest,tarpath)], shell=True)


#push archive to S3
# Key should be the variable related to a specific machine. Bucket should be universal for prod or stage

conn = boto.s3.connection.S3Connection(keyid,seckey)
new_bucket = conn.create_bucket('bobbys_test_bucket')
k = boto.s3.key.Key(new_bucket)
k.key = 'whut'
k.set_contents_from_filename("%s/backup.tar.gz" % (archdest))

#clean up mess


#!/usr/bin/env python


# scrpt to automatically generate tar.gz backups and push them to s3

import subprocess
from optparse import OptionParser
import boto

  
#pass tar to shell to create archive

backup = subprocess.call(["tar -zcf /home/bobby/python-stuff/tarspot/backup.tar.gz /home/bobby/Pictures/badgerstuff/"], shell=True)


#push archive to S3
















    

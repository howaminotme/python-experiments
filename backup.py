#!/usr/bin/env python


# scrpt to automatically generate tar.gz backups and push them to s3

import subprocess
from optparse import OptionParser
import Time

# loop to run weekely  

while True:

    backup = subprocess.call(["tar -zcf /home/bobby/python-stuff/tarspot/backup.tar.gz /home/bobby/Pictures/badgerstuff/"], shell=True)



















    time.sleep(604800)

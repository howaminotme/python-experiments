#scrpit for monitoring disk usage on the blog machine

import subprocess
import smtplib

df = subprocess.Popen(["df", "/dev/sda1"], stdout=subprocess.PIPE)

output = df.communicate()[0]

device, size, used, available, percent, mountpoint = \
    output.split("\n")[1].split()


print "The partition mounted on /dev/sda1 is %s full" % (percent)

#create variable that is an intiger for easier use in functions
usage_int = int(percent.replace("%", ""))


#funciton for taking aciton once threshold is reached - goal is to email someone if disk usage exceeds 80%
if usage_int > 80:

    sender = "help@readyforzero.com"
    recievers = ["engineering@readyforzero.com"]

    message = """From: From RFZ Blog <help@readyforzero.com>
    To: Enineering <engineering@readyforzero.com
    Subject: Blog Machine disk usage Warning

    This email is a friendly heads up that the Disk on the Blog machine is nearly full. Tell Ben to stop wiriting so much!
    """

    print "sending email to Ben informing him his Blog is about o explode"
    try:
        smtpObj = smtplib.SMTP("host")
        smtpObj.sendmail(sender,receivers,message)
        print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"

else:
    print "disk still has plenty of room!"



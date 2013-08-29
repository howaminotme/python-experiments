#scrpit for monitoring disk usage on the blog machine

import subprocess

df = subprocess.Popen(["df", "/dev/sda1"], stdout=subprocess.PIPE)

output = df.communicate()[0]

device, size, used, available, percent, mountpoint = \
    output.split("\n")[1].split()


print "The partition mounted on /dev/sda1 is %s full" % (percent)

#create variable that is an intiger for easier use in functions
usage_int = int(percent.replace("%", ""))


#funciton for taking aciton once threshold is reached - goal is to email someone if disk usage exceeds 80%
if usage_int > 80:
    print "sending email to Ben informing him his Blog is about o explode"
    #call sendgrid to email someone

else:
    print "disk still has plenty of room!"

import subprocess

df = subprocess.Popen(["df", "/dev/sda1"], stdout=subprocess.PIPE)

output = df.communicate()[0]

device, size, used, available, percent, mountpoint = \
    output.split("\n")[1].split()


print "The partition mounted on /dev/sda1 is %s full" % (percent)

usage_int = int(percent.replace("%", ""))

if usage_int > 80:
    print "sending email to Ben informing him his Blog is about o explode"
    #call sendgrid to email someone

else:
    print "disk still has plenty of room!"

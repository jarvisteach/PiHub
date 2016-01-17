import subprocess
import time
p = subprocess.Popen(['/usr/bin/mosquitto_sub','-v','-t','+/#'], stdout=subprocess.PIPE)
#p = subprocess.Popen('/usr/bin/mosquitto_sub', stdout=subprocess.PIPE)
time.sleep(.1)
p.terminate()
lines= p.communicate()[0]
myQueues = []
for a in lines.splitlines():
	myQueues.append(a.split()[0])

print(myQueues)

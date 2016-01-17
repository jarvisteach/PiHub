#!/usr/bin/python
import sys
import time
import subprocess
import socket
import os 
import smartups as UPS
import Adafruit_CharLCD as LCD
import fcntl
import struct

BUTTONS = [LCD.SELECT,LCD.LEFT,LCD.UP,LCD.DOWN,LCD.RIGHT];
QUEUE_NAMES = []

ups = UPS.SmartUPS()

#general functions
def getEmptyString(): return ""
def getString(val): return val

# System Stats
def getDate(): return time.strftime("%d/%m/%Y")
def getTime(): return time.strftime("%H:%M:%S")
def getIPaddress(): return socket.gethostbyname(socket.gethostname())

# Return CPU temperature as a character string                                      
def getCPUtemperature():
	res = os.popen('vcgencmd measure_temp').readline()
	res = (res.replace("temp=","").replace("'C\n",""))
	res = res + "'c"
	return res

def getRAMString():
	myRAM = getRAMinfo()
	return myRAM[1]+"/"+myRAM[0]

def getHDDString():
	myHDD = getDiskSpace()
	return myHDD[1] + "/" + myHDD[0]

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

def getQueueNames():
	global QUEUE_NAMES
	p = subprocess.Popen(['/usr/bin/mosquitto_sub','-v','-t','+/#'], stdout=subprocess.PIPE)
	time.sleep(.1)
	p.terminate()
	lines= p.communicate()[0]
	for a in lines.splitlines():
		QUEUE_NAMES.append(a.split()[0])
	return ""

def getMQTTMenu():
	global QUEUE_NAMES
	getQueueNames()
	myMenu = []
	myMenu.append(["*  MQTT Menu   *", "", "", False])
	for queue in QUEUE_NAMES:
		myMenu.append([queue, "getQueueVal " + queue, "", True])
	return myMenu

# Return % of CPU used by user as a character string                                
def getCPUuse():
	res = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline()).strip()
	if len(res) > 0: return res + "%"
	else: return "unknown"

# return host name as a string
def getHostName():
	return str(os.popen('hostname').readline()).strip()

# return mac address as a string
def getMacAddress():
	return str(os.popen("ifconfig -a | grep HWaddr | awk '/HWaddr/ {print $5}'").readline()).strip()

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def getQueueVal(val):
	p = subprocess.Popen(['/usr/bin/mosquitto_sub','-t',val], stdout=subprocess.PIPE)
	time.sleep(.1)
	p.terminate()
	lines= p.communicate()[0]
	for a in lines.splitlines():
		return a
	return "no message"

def getBattState(): return str(ups.readBattState())
def getBattCharged(): return str(ups.readCharged()) + "%"
def getBattTemp(): return str(ups.readBattTemperature())+ "'c"
def getBattVolt(): return str(ups.readBattVoltage()) + "v"
def getBattCurr(): return str(ups.readBattCurrent())
def getBattCapacity(): return str(ups.readBattCapacity()) + "/" + str(ups.readMaxCapacity())
def getBattTime(): return str(ups.readBattEastimatedTime())
def getBattHealth(): return str(ups.readBattHealth())
def getOutVolt(): return str(ups.readOutputVoltage())
def getOutCurr(): return str(ups.readOutputCurrent())

def get_e_ip_address(): return get_ip_address('eth0')
def get_w_ip_address(): return get_ip_address('wlan0')
def get_e_hw_address(): return get_hw_address('eth0')
def get_w_hw_address(): return get_hw_address('wlan0')

def get_ip_address(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15])
		)[20:24])
	except IOError:
		return "not found"

def get_hw_address(ifname):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
		return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
	except IOError:
		return "not found"

def reboot():
	print("Rebooting")
	os.system("reboot")

def shutdown():
	print("Shutting down")
	os.system("halt")

def exitLCD():
	print("Exiting LCD")
	sys.exit(0)

def getServiceState(myService):
	return os.popen(myService).readline()

def getApacheState():
	myState = getServiceState("sudo service apache2 status")
	if "NOT running" in myState: return "[DOWN]"
	else: return "[UP]"

def getMosquittoState():
	myState =  getServiceState("sudo service mosquitto status")
	if "is running" in myState: return "[UP]"
	else: return "[DOWN]"

def getMysqlState():
	myState = getServiceState("sudo service mysql status")
	if "stopped" in myState: return "[DOWN]"
	else: return "[UP]"
	
def getiBeaconState():
	myState = getServiceState("sudo service ibeacon status")
	if "UP" in myState: return "[UP]"
	else: return "[DOWN]"

def getDashingState():
	myState = getServiceState("sudo service dashingd status")
	if "UP" in myState: return "[UP]"
	else: return "[DOWN]"

def getSambaState():
	p = os.popen("sudo service samba status")
	i = 0
	while 1:
		line = p.readline()
		if "smbd is running" in line: return "[UP]"
		elif "smbd is not running" in line: return "[DOWN]"
	return "[DOWN]"

def getNodeJsState():
	return "[DOWN]"

def getSshState():
	myState = getServiceState("sudo service ssh status")
	if "is running" in myState: return "[UP]"
	else: return "[DOWN]"

def toggleApache():
	print "Toggling apache..."
	myService = "sudo service apache2 "
	if "UP" in getApacheState(): myService += "stop"
	else: myService += "start"
	os.popen(myService)

def toggleiBeacon():
	print "Toggling iBeacon..."
	myService = "sudo service ibeacon "
	if "UP" in getiBeaconState(): myService += "stop"
	else: myService += "start"
	print os.popen(myService)
	print myService

def toggleMosquitto():
	print "Toggling Mosquitto..."
	myService = "sudo service mosquitto "
	if "UP" in getMosquittoState(): myService += "stop"
	else: myService += "start"
	os.popen(myService)

def toggleMysql():
	print "Toggling MySQL..."
	myService = "sudo service mysql "
	if "UP" in getMysqlState(): myService += "stop"
	else: myService += "start"
	os.popen(myService)

def toggleSamba():
	print "Toggling Samba..."
	myService = "sudo service samba "
	if "UP" in getSambaState(): myService += "stop"
	else: myService += "start"
	os.popen(myService)

def toggleSshd():
	print "Toggling sshd..."
	myService = "sudo service ssh "
	if "UP" in getSshdState(): myService += "stop"
	else: myService += "start"
	os.popen(myService)

def toggleDashing():
	print "Toggling Dashing..."
	myService = "sudo service dashingd "
	if "UP" in getDashingState(): myService += "stop"
	else: myService += "start"
	os.popen(myService)

def toggleNodeJs():
	print "Toggling Node.js..."

def getNRFState():
	return "[DOWN]"

def buildMenu():
        menu = [
                [
                        ["* RPi Sys Menu *", "", "", False],
                        ["HOSTNAME:","getHostName", "", True],
                        ["IP eth0:","get_e_ip_address", "", True],
                        ["IP wlan0:","get_w_ip_address", "", True],
                        ["MAC eth0: ", "get_e_hw_address", "", False],
                        ["MAC wlan0: ", "get_w_hw_address", "", False],
                        ["DATE:","getDate", "", True],
                        ["TIME:","getTime", "", True],
                        ["CPU TEMP:","getCPUtemperature", "", True],
                        ["CPU USE:","getCPUuse", "", True],
                        ["RAM: ","getRAMString", "", True],
                        ["HDD: ","getHDDString", "", True],
                ],
                [
                        ["*  Services    *","", "", False],
                        ["Apache","getApacheState", "toggleApache", False],
                        ["MySQL","getMysqlState", "toggleMysql", False],
                        ["Mosquitto","getMosquittoState", "toggleMosquitto", False],
                        ["Samba","getSambaState", "toggleSamba", False],
                        ["sshd","getSshState", "toggleSshd", False],
                        ["Dashing","getDashingState", "toggleDashing", False],
                        ["Node.js","getNodeJsState", "toggleNodeJs", False],
                        ["iBeacon","getiBeaconState", "toggleiBeacon", False],
                ],
                getMQTTMenu(),
		[
			["*   NRF Menu   *", "", "", False],
			["Status", "getNRFState", "", True],
		],
                [
                        ["*  UPS Stats   *", "", "", False],
                        ["BATT STATE:", "getBattState", "", True],
                        ["BATT CHARGED:", "getBattCharged", "", True],
                        ["BATT TEMP:", "getBattTemp", "", True],
                        ["BATT VOLTAGE:", "getBattVolt", "", True],
                        ["BATT CURRENT:", "getBattCurr", "", True],
                        ["BATT CAPACITY:", "getBattCapacity", "", True],
                        ["BATT TIME:", "getBattTime", "", True],
                        ["BATT HEALTH:", "getBattHealth", "", True],
                        ["OUT VOLT:", "getOutVolt", "", True],
                        ["OUT CURR:", "getOutCurr", "", True],
                ],
                [
                        ["*  SYS Actions *", "", "", False],
                        ["Reboot", "", "reboot", False],
                        ["Shutdown", "", "shutdown", False],
                        ["Exit LCD", "", "exitLCD", False],
                ],
        ]
        return menu


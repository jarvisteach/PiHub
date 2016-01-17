#!/usr/bin/python
import lcdHelper
import time
import signal
import sys
import Adafruit_CharLCD as LCD

def signal_handler(signal, frame):
	global go
	print('Exiting gracefully...')
	lcdReset()
	lcdOff()
	go = False


def lcdToggle():
	global screenOn
	if screenOn:
		lcdOff()
	else:
		lcdOn()

def showDone(myWait=0.2):
	lcd.set_backlight(.5)
	lcd.set_color(0, 0, 1)
	time.sleep(myWait)
	lcd.set_color(1, 1, 1)
	lcd.set_backlight(1)

def showError(myWait=0.2):
	lcd.set_backlight(.5)
	lcd.set_color(1, 0, 0)
	time.sleep(myWait)
	lcd.set_color(1, 1, 1)
	lcd.set_backlight(1)

def lcdOn():
	global screenOn
	screenOn = True
	lcd.set_color(1, 1, 1)
	lcd.enable_display(True)
	lcd.set_backlight(1)
	scrollLines()

def lcdOff():
	global screenOn
	screenOn = False
	lcd.enable_display(False)
	lcd.set_backlight(0)

def lcdReset():
	lcd.clear()
	lcd.set_cursor(0,0) # col, row

def showTopLine(myColPos, myLinePos):
	global menu
	lcd.set_cursor(0,0)
	lcd.message(menu[myColPos][myLinePos][0])

def showBottLine(myColPos, myLinePos):
	global menu, lastUpdateTime
	lcd.set_cursor(0,1)
	lcd.message(getMessage(menu[myColPos][myLinePos][1]))
	lastUpdateTime = time.time()

def scrollLines():
	global linePos, colPos
	lcd.clear()
	showTopLine(colPos,linePos)
	showBottLine(colPos, linePos)


def buttonPressed(button):
	global linePos, colPos, menu
	if button == LCD.UP:
		if linePos > 0:
			linePos -=1
			scrollLines()
		else:
			showDone()
	elif button == LCD.DOWN:
		if linePos < len(menu[colPos])-1:
			linePos +=1
			scrollLines()
		else:
			showDone()
	elif button == LCD.LEFT:
		if colPos > 0:
			colPos -=1
			linePos = 0
			scrollLines()
		else:
			showDone()
	elif button == LCD.RIGHT:
		menu = lcdHelper.buildMenu()
		if colPos < len(menu) - 1:
			colPos +=1
			linePos = 0
			scrollLines()
		else:
			showDone()
	elif button == LCD.SELECT:
		executeAction(menu[colPos][linePos][2])

def getMessage(myAction):
	print (myAction)
	myAction = myAction.strip()
	result = ""
	if len(myAction) > 0:
		myActions = myAction.split()
		funcName = getattr(lcdHelper, myActions[0])
		if len(myActions) == 1:
			result = funcName()
		else:
			result = funcName(myActions[1])
		if len(result) > 0:
			result = "> " + result

	spaces = 16 - len(result)
	for i in range(0, spaces-1): result = result + " "
	return result

def executeAction(myAction):
	if len(myAction) > 0:
		if confirm():
			lcdOff()
			funcName = getattr(lcdHelper, myAction)
			result = funcName()
		else:
			scrollLines()
	else:
		showError()
		return

def confirm():
	global lastButton, lastButtonTime
	lcd.set_cursor(0,1)
	lcd.message(">> Are you sure?")
	startTime = nowTime = time.time()
	while startTime > nowTime -3:
		for button in lcdHelper.BUTTONS:
			nowTime = time.time()
			if lcd.is_pressed(button):
				if button != lastButton or nowTime > lastButtonTime + .2:
					lastButton = button
					lastButtonTime = nowTime
					
					if button == LCD.SELECT:
						lcd.set_cursor(0,1)
						lcd.message(">> CONFIRMED    ")
						time.sleep(1)
						return True
					else:
						lcd.set_cursor(0,1)
						lcd.message(">> CANCELLED    ")
						showError(.5)
						return False

	lcd.set_cursor(0,1)
	lcd.message(">> TIME UP      ")
	lastButtonTime = nowTime
	showError(1)
	return False

############### START HERE ###############

# the LCD object
lcd = LCD.Adafruit_CharLCDPlate()

# these are our position in the menu array
menu = lcdHelper.buildMenu()
linePos = 0
colPos = 0

screenOn = False

# the last button pnd time it was pressed - for debouncing
lastButton = -1
lastButtonTime  = time.time()

# last time the bottom line was refreshed
lastUpdateTime = time.time()

# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
go = True	#this will be set to alse if we receive a sig

# make sure LCD is cleared up
lcdReset()
lcdOn()


while True == go:
	timeNow = time.time()

	# if more than a second since last update - refresh
	if screenOn and timeNow - lastUpdateTime > 1 and menu[colPos][linePos][3] :
		showBottLine(colPos,linePos)

	# Loop through each button and check if it is pressed.
	for button in lcdHelper.BUTTONS:
		if lcd.is_pressed(button):
			if not screenOn: lcdOn()
			else:
				if button != lastButton or timeNow > lastButtonTime + .2:
					lastButton = button
					buttonPressed(button)
				else: pass
			lastButtonTime = timeNow
	time.sleep(0.1)

	# put display to sleep if 10 seconds passed since button pressed
	if screenOn and timeNow > lastButtonTime + 10: lcdOff()

sys.exit(0)

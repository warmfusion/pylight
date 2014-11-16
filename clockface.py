#!/usr/bin/env python

# Test code for Adafruit LED Pixels, uses hardware SPI

import RPi.GPIO as GPIO, time, os

from datetime import datetime 

DEBUG = 1
GPIO.setmode(GPIO.BCM)

def slowspiwrite(clockpin, datapin, byteout):
	GPIO.setup(clockpin, GPIO.OUT)
	GPIO.setup(datapin, GPIO.OUT)
	for i in range(8):
		if (byteout & 0x80):
			GPIO.output(datapin, True)
		else:
			GPIO.output(clockpin, False)
		byteout <<= 1
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)


TOP_LED=7
LED_SIZE=32
LED_POWER=127
LED_SPREAD=2 / float(LED_SIZE)


SPICLK = 18
SPIDO = 17

def writestrip(pixels):
	spidev = file("/dev/spidev0.0", "w")
	for i in range(len(pixels)):
		spidev.write(chr((pixels[i]>>16) & 0xFF))
		spidev.write(chr((pixels[i]>>8) & 0xFF))
		spidev.write(chr(pixels[i] & 0xFF))
	spidev.close()
	time.sleep(0.002)

def Color(r, g, b):
	return ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def setpixelcolor(pixels, n, r, g, b):
	if (n >= len(pixels)):
		return
	pixels[n] = Color(r,g,b)

def setpixelcolor(pixels, n, c):
	if (n >= len(pixels)):
		return
	pixels[n] = c

def colorwipe(pixels, c, delay):
	for i in range(len(pixels)):
		setpixelcolor(pixels, i, c)
		writestrip(pixels)
		time.sleep(delay)		

#colorwipe(ledpixels, Color(255, 0, 0), 0.01)
#colorwipe(ledpixels, Color(0, 255, 0), 0.01)
#colorwipe(ledpixels, Color(0, 0, 255), 0.01)


# target, and position are a float between 0 and 1
# This function calculates a power rating to return
# for a given position and target on the strip
# such that the brightness scales linearly from the
# target out to the spread width on either side of
# the target LED.
def calcSpread(target, position, power):

  ledDist = abs(target - position) # How far is the target from the position
  ledDist = ledDist if ledDist <= LED_SIZE/2 else abs(ledDist - LED_SIZE) # Wrap around edge
  distRatio = ledDist / LED_SIZE              # as a ratio of the whole

  # If the LED is outside our spread then, just return
  if distRatio > LED_SPREAD: return 0

  # Now calculate what power to return;
#  print "t: %f, p: %f, s: %f ; dist: %f" % (target, position, LED_SPREAD, distRatio)  
  offset = (LED_SPREAD - distRatio) / LED_SPREAD
  return int(power * offset)
  

def buildClockface(pixels, clock, wait=0):
  # Don't cope with 24 hour clocks :-)
  hour = clock.hour if clock.hour < 12 else clock.hour - 12

  min = clock.minute
  sec = clock.second

  h = ((hour + (min / 60.0)) / 12.0) * len(pixels);
  m = ((min +  (sec / 60.0))/ 60.0) * len(pixels);
  s = ((sec + (clock.microsecond/1000000.0) )  / 60.0) * len(pixels);



  for j in range(LED_SIZE):
    led=(j+TOP_LED) % LED_SIZE # Rotate around to so the selected TOP_LED is at 12:00
    setpixelcolor(pixels, led, Color(
           calcSpread(h,j,LED_POWER),
           calcSpread(m,j,LED_POWER),
           calcSpread(s,j,LED_POWER))
          )
  


# Run a 12 hour cycle for testing.
h=0;m=0;s=0

#for h in range(12):
#  for m in range(60):
#    for s in xrange(0,60,2):
#      pixels =[0] * LED_SIZE
#      buildClockface(pixels, datetime.strptime("%s:%s:%s" % (h,m,s), "%H:%M:%S"))
#      writestrip(pixels)
#      time.sleep(0.001)

while True:
  pixels =[0] * LED_SIZE
  now = datetime.now().time()
  buildClockface(pixels, now)
  writestrip(pixels)
  time.sleep(0.01)

#while True:
#	rainbowCycle(ledpixels, 0.01)

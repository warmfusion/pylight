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


SPICLK = 18
SPIDO = 17

ledpixels = [0] * 32

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

def Wheel(WheelPos):
	if (WheelPos < 85):
   		return Color(WheelPos * 3, 255 - WheelPos * 3, 0)
	elif (WheelPos < 170):
   		WheelPos -= 85;
   		return Color(255 - WheelPos * 3, 0, WheelPos * 3)
	else:
		WheelPos -= 170;
		return Color(0, WheelPos * 3, 255 - WheelPos * 3)

def rainbowCycle(pixels, wait):
	for j in range(256): # one cycle of all 256 colors in the wheel
    	   for i in range(len(pixels)):
# tricky math! we use each pixel as a fraction of the full 96-color wheel
# (thats the i / strip.numPixels() part)
# Then add in j which makes the colors go around per pixel
# the % 96 is to make the wheel cycle around
      		setpixelcolor(pixels, i, Wheel( ((i * 256 / len(pixels)) + j) % 256) )
	   writestrip(pixels)
	   time.sleep(wait)


#colorwipe(ledpixels, Color(255, 0, 0), 0.01)
#colorwipe(ledpixels, Color(0, 255, 0), 0.01)
#colorwipe(ledpixels, Color(0, 0, 255), 0.01)

LED_SIZE=32
LED_POWER=64
LED_SPREAD=1 / float(LED_SIZE)


# target, and position are a float between 0 and 1
def calcSpread(target, position, power):

  ledDist = abs(target - position) # distance between points
  distRatio = ledDist / LED_SIZE   # as a ratio of the whole

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

  h = (hour / 12.0) * len(pixels);
  setpixelcolor(pixels, int(h), Color(LED_POWER,0,0))

  m = (min / 60.0) * len(pixels);
  setpixelcolor(pixels, int(m), Color(0,0,LED_POWER))
  
  s = ((sec + (now.microsecond/1000000.0) )  / 60.0) * len(pixels);
  for j in range(LED_SIZE):
    setpixelcolor(pixels, j, Color(
           calcSpread(h,j,LED_POWER),
           calcSpread(m,j,LED_POWER),
           calcSpread(s,j,LED_POWER))
          )
  

while True:
  pixels =[0] * LED_SIZE
  now = datetime.now().time()
  buildClockface(pixels, now)
  writestrip(pixels)

#while True:
#	rainbowCycle(ledpixels, 0.01)

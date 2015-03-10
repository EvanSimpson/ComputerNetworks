import Rpi.GPIO as GPIO
import time

def prepare_pins(dtpin = 17, ctpin = 18, crpin = 22, drpin = 23):
	GPIO.setmode(GPIO.bcm)
	GPIO.setup(dtpin,GPIO.OUT)
	GPIO.setup(ctpin,GPIO.OUT)
	GPIO.setup(crpin,GPIO.IN)
	GPIO.setup(drpin,GPIO.IN)

def turn_high(pin):
	GPIO.output(pin,GPIO.HIGH)

def turn_low(pin):
	GPIO.output(pin,GPIO.LOW)

def delay(t):
	time.sleep(t)

def read_pin(pin):
	return GPIO.input(pin)

def transmit(data, dtpin=17,ctpin = 18, crpin = 22, duration = .25):
	prepare_pins(dtpin,ctpin,crpin)
	counter = 0
	while(True):
		busy = read_pin(crpin)
		if (busy == 0):
			counter = counter + 1
		if (busy == 1):
			counter = 0
		if counter >= 8:
			break
		delay(.1)
	turn_high(ctpin)
	for i in range(len(data)):	
		if data[i]==1:
			turn_high(dtpin)
		else:
			turn_low(dtpin)
		delay(duration)
	turn_low(dtpin)
	turn_low(ctpin)



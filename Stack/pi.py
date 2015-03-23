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

def transmit(data, dtpin=17,ctpin = 18, crpin = 22, drpin = 23, duration = .0025):
	prepare_pins(dtpin,ctpin,crpin,drpin)
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

def receive(duration=.0025, drpin=23):
    prepare_pin(pin)
    bin_string = ""
    buffer = []
    msg_start = False
    zero_cnt = 0
    while 1:
        if read_pin(pin):
            msg_start = True
            buffer.append(1)
            zero_cnt = 0
            delay(duration)
        elif msg_start:
            zero_cnt+=1
            if zero_cnt > 100:
                msg_start = False
                break
            buffer.append(0)
            delay(duration)
    zeroes = 0
    ones = 0
    if buffer[0] == 1:
        ones = 1
    else:
        zeroes = 1
    for i in range(len(buffer) - 1):
        if buffer[i+1] == buffer[i]:
            if buffer[i+1] == 0:
                zeroes += 1
            else:
                ones += 1
        else:
            if buffer[i+1] == 0:
                zeroes = 1
                if ones > 8:
                    bin_string += "111"
                else:
                    bin_string += "1"
                ones = 0
            else:
                ones = 1
                if zeroes <= 8:
                    bin_string += "0"
                elif zeroes > 8 and zeroes <= 26:
                    bin_string += "000"
                else:
                    bin_string += "0000000"
                zeroes = 0
    print(bin2message(bin_string))
    return bin2message(bin_string)	


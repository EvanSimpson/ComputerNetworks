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
	prepare_pins()
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


def receive(drpin=23):
    dur = .0025
    prepare_pins()
    times = []
    def cbf(channel):
        times.append(time.time())
    GPIO.add_event_detect(chanel,GPIO.BOTH,callback = cbf)
    while(True):
        if time.time > times[-1] + dur*20:
            yield process(times)
            times = []

def process(times):
    bin = ""
    dts = [x - y for (x,y) in zip(times[1:],times[:-1])]
    for i in range(len(dts)):
        if i%2:
            if dt[i]<dur*2:
                bin = bin + '1'
            else:
                bin = bin + '111'
        else:
            if dt[i]<dur*2:
                bin = bin + '0'
            elif dt[i]<dur*5:
                bin = bin + '000'
            else:
                bin = bin + '0000000'
    return bin

if __name__ == "__main__":
    data = receive()
    print(next(data))
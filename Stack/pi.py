import RPi.GPIO as GPIO
import time
import threading

def prepare_pins(dtpin = 17, ctpin = 18, crpin = 22, drpin = 23):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(dtpin,GPIO.OUT)
	GPIO.setup(ctpin,GPIO.OUT)
	GPIO.setup(crpin,GPIO.IN)
	GPIO.setup(drpin,GPIO.IN)

def kill():
        GPIO.cleanup()

def turn_high(pin):
	GPIO.output(pin,GPIO.HIGH)

def turn_low(pin):
	GPIO.output(pin,GPIO.LOW)

def delay(t):
	time.sleep(t)

def read_pin(pin):
	return GPIO.input(pin)

def transmit(data, dtpin=17,ctpin = 18, crpin = 22, drpin = 23, duration = 1):
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


def receive(lock, drpin=23,crpin = 22):
    global received_packet
    prepare_pins()
    times = []
    def cbf(channel):
        times.append(time.time())
    def cbf2(channel):
        times.append(time.time())
        if not(read_pin(22)):
             times.append(-1)
    GPIO.add_event_detect(crpin,GPIO.BOTH,callback = cbf2)
    GPIO.add_event_detect(drpin,GPIO.BOTH,callback = cbf)
    while(True):
        if (len(times)>0) and (times[-1]==-1):
            lock.aquire(blocking=True)
            try:
                received_packet = process(times[1:-1])
            finally:
                lock.release()
            #yield process(times[1:-1])

            times = []

def process(times):
    bin = ""
    buffer = []
    dur = .001
    dts = [x - y for (x,y) in zip(times[1:],times[:-1])]
    flag = False
    for i in range(len(dts)):  
        if flag:
           if dts[i]<dur*2:
               bin = bin + '1'
           else:
               bin = bin + '111'
        else:
           if dts[i]<dur*2:
               bin = bin + '0'
           elif dts[i]<dur*5:
               bin = bin + '000'
           else:
               bin = bin + '0000000'
        flag = not(flag)
    return bin

if __name__ == "__main__":
    data = receive()
    print(next(data))

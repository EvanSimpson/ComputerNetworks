import RPi.GPIO as GPIO
import time

def prepare_pins_in(data_pin = 18,carrier_pin = 23):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(carrier_pin,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(data_pin,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def prepare_pins_out(data_pin = 18,carrier_pin = 23):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(carrier_pin,GPIO.OUT)
	GPIO.setup(data_piN,GPIO.OUT)

def kill():
	GPIO.cleanup()

def turn_high(pin):
	GPIO.output(pin,GPIO.HIGH)

def turn_low(pin):
	GPIO.output(pin,GPIO.LOW)

def read_pin(pin):
	return GPIO.input(pin)

def transmit(data, data_pin = 18, carrier_pin = 23, duration = .001):
	prepare_pins_in(data_pin,carrier_pin)
	counter = 0
	while(True):
		busy = read_pin(carrier_pin)
		if (busy == 0):
			counter = counter + 1
		if (busy == 1):
			counter = 0
		if counter >= 8:
			break
		time.sleep(.01)
	prepare_pins_out()
	turn_high(carrier_pin)
	for i in range(len(data)):
		if data[i]==1:
			turn_high(data_pin)
		else:
			turn_low(data_pin)
		time.sleep(duration)
	turn_low(data_pin)
	turn_low(carrier_pin)

def receive(data_pin=18, carrier_pin = 23, duration = .001):
	prepare_pins_in(data_pin,carrier_pin)
	times = []
	def data_callback(channel):
		times.append(time.time())
	def carrier_callback(channel):
		times.append(time.time())
		if not(read_pin(carrier_pin)):
			times.append(-1)
	GPIO.add_event_detect(data_pin,GPIO.BOTH,callback = data_callback)
	GPIO.add_event_detect(carrier_pin,GPIO.BOTH,callback = carrier_callback)
	while(True):
		if (len(times)>0) and (times[-1] == -1):
			yield process(times,duration)
			times = []

def process(times,duration):
	binput = ""
	delta_times = [x - y for (x,y) in zip(times[1:],times[:-1])]
	flag = False
	for i in range(len(delta_times)):
		if flag:
			if delta_times[i]<duration*2:
				binput = binput + '1'
			else:
				binput = binput + '111'
		else:
			if delta_times[i]<duration*2:
				binput = binput + '0'
			elif delta_times[i]<duration*5:
				binput = binput + '000'
			else:
				binput = binput + '0000000'
		flag = not(flag)
		return binput

if __name__ == "__main__":
	transmit("11101010001000000010111")
	kill()

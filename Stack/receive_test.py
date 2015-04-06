import RPi.GPIO as GPIO
import time

def prepare_pins(data_transmit_pin = 18, carrier_transmit_pin = 17, carrier_read_pin = 22, data_read_pin = 23):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(data_transmit_pin,GPIO.OUT)
	GPIO.setup(carrier_transmit_pin,GPIO.OUT)
	GPIO.setup(carrier_read_pin,GPIO.IN)
	GPIO.setup(data_read_pin,GPIO.IN)

def kill():
	GPIO.cleanup()

def turn_high(pin):
	GPIO.output(pin,GPIO.HIGH)

def turn_low(pin):
	GPIO.output(pin,GPIO.LOW)

def read_pin(pin):
	return GPIO.input(pin)

def transmit(data, data_transmit_pin=18, carrier_transmit_pin = 17, carrier_read_pin = 22, data_read_pin = 23, duration = 1):
	prepare_pins()
	counter = 0
	while(True):
		busy = read_pin(carrier_read_pin)
		if (busy == 0):
			counter = counter + 1
		if (busy == 1):
			counter = 0
		if counter >= 8:
			break
		time.sleep(.1)
	turn_high(carrier_transmit_pin)
	for i in range(len(data)):
		if data[i]==1:
			turn_high(data_transmit_pin)
		else:
			turn_low(data_transmit_pin)
		time.sleep(duration)
	turn_low(data_transmit_pin)
	turn_low(carrier_transmit_pin)

def receive(data_read_pin=23):
	prepare_pins()
	times = []
	def data_callback(channel):
		times.append(time.time())
	duration = .01
	GPIO.add_event_detect(data_read_pin,GPIO.BOTH,callback = data_callback)
    while(True):
        if (len(times)>0) and (time.time() > times[-1] + duration*10):
            yield process(times)
            times = []

def process(times):
	binput = ""
	duration = .01
	delta_times = [x - y for (x,y) in zip(times[1:],times[:-1])]
	flag = False
	for i in range(len(delta_times)):
		if flag:
			if delta_times[i]<duration*2:
				binput = binput + '1'
			else:
				binput = binput + '111'
		else:
			if delta_times[i]<duration*2
				binput = binput + '0'
			elif delta_times[i]<duration*5:
				binput = binput + '000'
			else:
				binput = binput + '0000000'
		flag = not(flag)
		return binput

if __name__ == "__main__":
	data = receive()
	print(next(data))
    kill()

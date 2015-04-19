import RPi.GPIO as GPIO
import time

def prepare_pins_in(*argv):
	GPIO.setmode(GPIO.BCM)
	for pin in argv:
		GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def prepare_pins_out(*argv):
	GPIO.setmode(GPIO.BCM)
	for pin in argv:
		GPIO.setup(pin,GPIO.OUT)

def kill():
	GPIO.cleanup()

def turn_high(pin):
	GPIO.output(pin, GPIO.HIGH)

def turn_low(pin):
	GPIO.output(pin, GPIO.LOW)

def read_pin(pin):
	return GPIO.input(pin)

def transmit(data, data_pin = 18, carrier_pin = 23, duration = 0.08, debug=False):
	prepare_pins_in(data_pin,carrier_pin)
	counter = 0
	print(data)
	while(True):
		busy = read_pin(carrier_pin)
		if (busy == 0):
			counter = counter + 1
		if (busy == 1):
			counter = 0
		if counter >= 8:
			break
		time.sleep(duration)
	prepare_pins_out(data_pin, carrier_pin)
	turn_high(carrier_pin)
	for i in range(len(data)):
		if debug:
			print(data[i])
		if data[i]=="1":
			turn_high(data_pin)
		else:
			turn_low(data_pin)
		time.sleep(duration)
	turn_low(data_pin)
	time.sleep(duration)
	turn_low(carrier_pin)

def receive(lock, recv_flag, data_pin=18, carrier_pin = 23, duration=0.08, debug=False):
	prepare_pins_in(data_pin, carrier_pin)
	times = []
	def data_callback(channel):
		times.append(time.time())
		print("Data edge")
	def carrier_callback(channel):
		times.append(time.time())
		if not read_pin(carrier_pin):
			times.append(-1)
			if debug:
				print("Carrier down")
		elif debug:
			print("Carrier up")
	GPIO.add_event_detect(data_pin, GPIO.BOTH, callback=data_callback)
	GPIO.add_event_detect(carrier_pin, GPIO.BOTH, callback=carrier_callback)
	if lock.acquire():
		while(recv_flag.flag):
			lock.release()
			if (len(times)>0) and (times[-1] ==-1):
				yield process(times[:-1], duration)
				times = []
			lock.acquire(blocking=True)
	lock.release()

def process(times, duration):
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
	return binput[1:-1]

if __name__ == "__main__":
	import socket

	gpio_serve_address = ('127.0.0.1', 5003)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(bytearray('1', encoding="UTF-8"), gpio_serve_address)

	while True:
		try:
			(data_in, address_in) = sock.recvfrom(1024)
			print(data_in.decode("UTF-8"))
		except socket.error:
			continue
		except:
			break

	sock.close()

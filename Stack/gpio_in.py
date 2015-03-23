from pi_layer import *

def gpio_in():
	while(True):
		data = receive()
		if data:
			print(data)


if __name__=="__main__":
	gpio_in()
from pi import *

def gpio_out():
	while True:
		text_input = input()
		if text_input:
			transmit(text_input)


if __name__=="__main__":
	gpio_out()
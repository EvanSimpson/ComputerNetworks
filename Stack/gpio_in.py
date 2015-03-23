#from pi import *
import sys
import fileinput

def gpio_in():
	while True:
		try:
			data = input()
			print("THE DATA IS " + data)
		except EOFError:
			pass

if __name__=="__main__":
	gpio_in()
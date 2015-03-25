#from pi import *
import sys
import subprocess

def gpio_in():
	while True:
		try:
			data = input()
			print(data)
			if data != '':
				subprocess.call(["python3", "new_app.py"])
		except EOFError:
			pass

if __name__=="__main__":
	gpio_in()
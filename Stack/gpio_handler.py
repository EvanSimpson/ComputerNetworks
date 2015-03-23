import sys
import subprocess

def gpio_handler():

	#port_subprocess = subprocess.Popen(["python3", "generate_port.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	in_process = subprocess.Popen(["python3","gpio_in.py"], stdin=subprocess.PIPE, universal_newlines = True) #,"192.168.0.1","45321"])

	while True:
		f = open(in_process.stdin)
		for line in f:
			if line != '':
				print(line)
	#print(sys.stdin.readline())
	# if incoming:
	# 	[port_output, err] = port_subprocess.communicate(input="1")
	# 	port_num = port_output.readline()
	# 	print("port num is " + port_numh)
	# 	subprocess.call(["python3", "game/Controller.py", own_ip, port_num])

if __name__ == "__main__":
	while True:
		gpio_handler()
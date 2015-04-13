from gpio_serve import GPIOServe
from stack import Stack
import threading

def run_gpio_server():
	gpio_server = GPIOServe()
	gpio_server.listen()

def run_stack_server(as_router):
	stack_server = Stack(is_router=as_router)
	Stack.receive_input()

def read_config_file():
	config_file = open('config.txt', 'r')
	lines = config_file.readlines()
	params = {}
	for line in lines:
		split_line = line.split(":")
		params[split_line[0]] = split_line[1]

	return params

if __name__=="__main__":
	params = read_config_file()
	print(params)

	gpio_thread = threading.Thread(target=run_gpio_server)
	gpio_thread.start()

	stack_thread = threading.Thread(target=run_stack_server, args=(eval(params['is_router'])))
	stack_thread.start()

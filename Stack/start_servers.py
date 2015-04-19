from time import sleep
from gpio_serve import GPIOServe
from stack import Stack
from generate_port import PortAuthority
import threading
from read_config import get_config_params

def run_gpio_server():
	gpio_server = GPIOServe()
	gpio_server.listen()

def run_stack_server(as_router):
	stack_server = Stack(is_router=as_router)
	stack_server.receive_input()

def run_port_server():
	port_server = PortAuthority()
	port_server.listen()

if __name__=="__main__":
	params = get_config_params()

	gpio_thread = threading.Thread(target=run_gpio_server)
	gpio_thread.start()

	generateport_thread = threading.Thread(target=run_port_server)
	generateport_thread.start()

	sleep(1)
	is_router = eval(params['is_router'])
	mac_address = params['MAC']
	print("is router : " + str(is_router))
	stack_thread = threading.Thread(target=run_stack_server, args=(mac_address, is_router,))
	stack_thread.start()

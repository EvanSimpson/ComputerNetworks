# from bj import *
# from UDP import UDP, UDPHeader, encode_udp, decode_udp
# from datalink import Mac, encode_message, decode_message
# from physical import physical_down, physical_up
# from pi import transmit, receive
import subprocess
import sys

class Stack():

	def __init__(self):
		# physical_layer = BJ(transmit, receive)
		# morse_layer = BJ(physical_down, physical_up)
		# mac_layer = BJ(encode_message, decode_message)
		# udp_layer = BJ(encode_udp, decode_udp)

		# self.stack = BJ_Stack([udp_layer, mac_layer, morse_layer, physical_layer])
		
		handler_process = subprocess.Popen(["python3","gpio_handler.py"])
		
		#port_subprocess = subprocess.Popen(["python3", "generate_port.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#subprocess.Popen(["python3","gpio_in.py"]) 


		while True:
			pass
		
		#out_subprocess = subprocess.call(["python3","gpio_out.py"]) #,"192.168.0.1","45321"])
		

	def send_data(self, message_to_send):
		udp_obj = self.initialize_udp(message_to_send)
		return stack.descend(udp_obj)

	def handle_received_data(self, message_received):
		if message_received == "1":
			self.becomeHost()
		if message_received == "2":
			self.becomeClient()
		return stack.ascend(message_received)

	def becomeHost(self):
		'''
		create a socket with own ip adress and a port number
		'''
		pass

	def becomeClient(self):
		'''
		create a socket with host ip adress and a port number
		'''

	def initialize_udp(message_to_send):
		udp_header = UDPHeader()
		udp_header.setFields('01', '02', bytearray(message_to_send, encoding='UTF-8'))
		return UDP(udp_header, "CA", "BD")

if __name__ == "__main__":
	stack = Stack()
from bj import *
from UDP import UDP, UDPHeader, encode_udp, decode_udp
from datalink import Mac, encode_message, decode_message
from physical import physical_down, physical_up
from pi import transmit, receive
from gpio_in import gpio_in
import subprocess

class Stack():

	def __init__(self):
		physical_layer = BJ(transmit, receive)
		morse_layer = BJ(physical_down, physical_up)
		mac_layer = BJ(encode_message, decode_message)
		udp_layer = BJ(encode_udp, decode_udp)

		self.stack = BJ_Stack([udp_layer, mac_layer, morse_layer, physical_layer])

		gpio_in()
		gpio_out()



	def send_data(self, message_to_send):
		udp_obj = self.initialize_udp(message_to_send)
		return stack.descend(udp_obj)

	def receive_data(self, message_received):
		return stack.ascend(message_received)

	def initialize_udp(message_to_send):
		udp_header = UDPHeader()
		udp_header.setFields('01', '02', bytearray(message_to_send, encoding='UTF-8'))
		return UDP(udp_header, "CA", "BD")

if __name__ == "__main__":
	stack = Stack()
	stack.receive
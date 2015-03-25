import socket
from bj import *
from UDP import UDP, UDPHeader, encode_udp, decode_udp
from datalink import Mac, encode_message, decode_message
from morse import morse_down, morse_up
#from pi import transmit, receive

class Stack():

	def __init__(self):
		#physical_layer = BJ(transmit, receive)
		morse_layer = BJ(morse_down, morse_up)
		mac_layer = BJ(encode_message, decode_message)
		udp_layer = BJ(encode_udp, decode_udp)

		self.stack = BJ_Stack([udp_layer, mac_layer, morse_layer])
		
		game_socket = 5000
		pi_socket = 5001

		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind(socket.gethostbyname(socket.gethostname()), game_socket)
		self.serversocket.bind(socket.gethostbyname(socket.gethostname()), pi_socket)

	def listen(self):
		while True:
			try:
				(input_from_pi, pi_address) = self.serversocket.recvfrom(1024)
				if pi_address ==  
			except:
				continue
		
	def send_data(self, message_to_send):
		udp_obj = self.initialize_udp(message_to_send)
		return self.stack.descend(udp_obj)

	def listen(self):
		received_packet = receive()
		return next(received_packet)

	def handle_received_packet(self, message_received):
		return self.stack.ascend(message_received)

	def initialize_udp(self, message_to_send):
		udp_header = UDPHeader()
		udp_header.setFields('01', '02', bytearray(message_to_send, encoding='UTF-8'))
		return UDP(udp_header, "CA", "BD")

if __name__ == "__main__":
	stack = Stack()
	print(stack.handle_received_packet(stack.send_data("HELLO WORLD")))
import sys
import socket
import json
from bj import *
from UDP import UDP, UDPHeader, encode_udp, decode_udp
from datalink import Mac, encode_message, decode_message
from morse import morse_down, morse_up
# from pi import transmit, receive
import threading

lock = threading.Lock()

class Stack():

	def __init__(self):
		self.active_game_ports = {}
		self.setup_bj()
		self.setup_servers()

	#setup functions

	def setup_bj(self):
		morse_layer = BJ(morse_down, morse_up)
		mac_layer = BJ(encode_message, decode_message)
		udp_layer = BJ(encode_udp, decode_udp)

		self.joesocket_commands = {
			"bind": self.joesocket_bind,
			"close": self.joesocket_close,
			"sendto": self.joesocket_sendto
		}

		self.stack = BJ_Stack([udp_layer, mac_layer, morse_layer])

	def setup_servers(self):
		self.game_server_port = 5000
		self.localhost = '127.0.0.1'

		self.game_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.game_server_socket.bind((self.localhost, self.game_server_port))

	#listening out over joesocket and gpio

	def listen_for_input(self):
		#gpio_thread = self.listen_over_gpio()
		while True:

			# lock.acquire(blocking=True)
			# try:
			# 	if (received_packet!=""):
			# 		self.handle_input_from_gpio(received_packet)
			# finally:
			# 	lock.release()

			self.listen_for_games()

	# def listen_over_gpio(self):
	# 	gpio_thread = threading.Thread(target=receive, args=[lock], name="gpio_receive_thread")
	# 	gpio_thread.start()
	# 	return gpio_thread

	def listen_for_games(self):
		try:
			(input_from_client, client_address) = self.game_server_socket.recvfrom(1024)
			self.handle_input_from_client(input_from_client, client_address)
		except KeyboardInterrupt:
			# continue
			self.game_server_socket.close()
			sys.exit()

	#handling inputs

	def handle_input_from_client(self, message_bytearray, client_address):

		parsed_message = json.loads(message_bytearray.decode("UTF-8"))

		if parsed_message['params']['source_address'][1] not in self.active_game_ports:
			self.add_new_client(parsed_message['params']['source_address'][1], client_address)

		self.joesocket_commands[parsed_message['command']](**parsed_message['params'])


	def add_new_client(self, port_letter, client_address):
		self.active_game_ports[port_letter] = client_address

	# def handle_input_from_gpio(self, message_received):
	# 	udp_input = self.stack.ascend(message_received)
	# 	destination_port = udp_input.udp_header._destinationPort
	# 	if destination_port in self.active_game_ports:
	# 		destination_address = self.active_game_ports[destination_port]

	# 		payload = udp_input.udp_header._payload
	# 		source = (udp_input.ip_header._sourceAddress, udp_input.udp_header._sourcePort)

	# 		to_send = json.dumps([{'payload': payload, 'address': source}])
	# 		game_server_socket.sendto(to_send, destination_address)

	# functions called on joesocket commands

	def joesocket_bind(self, address):
		port = address[1]
		self.send_acknowledgement(self.active_game_ports[port])

	def joesocket_close(self, address):
		port = address[1]
		if port in active_game_ports:
			active_game_ports.pop(port)
		self.send_acknowledgement(self.active_game_ports[port])

	def joesocket_sendto(self, source_address, destination_address, data):
		self.send_message_over_gpio(source_address, destination_address, data)
		self.send_acknowledgement(self.active_game_ports[source_address[1]])

	def send_acknowledgement(self, client_address):
		return_message = bytearray(json.dumps({"Error": 0}), encoding="UTF-8")
		self.game_server_socket.sendto(return_message, client_address)

	#sending data over gpio based on input from joesocket

	def send_message_over_gpio(self, source_address, destination_address, message_to_send):
		udp_obj = self.initialize_udp(source_address, destination_address, message_to_send)
		to_transmit_string = self.stack.descend(udp_obj)
		to_transmit = bytearray(to_transmit_string, encoding='UTF-8')
		# self.gpio_server_socket.sendto(to_transmit, self.gpio_address)

	def initialize_udp(self, source_address, destination_address, message_to_send):
		udp_header = UDPHeader()
		udp_header.setFields(source_address[1], destination_address[1], bytearray(message_to_send, encoding="UTF-8"))
		return UDP(udp_header, srcAddr=source_address[0], destAddr=destination_address[0])

if __name__ == "__main__":
	stack = Stack()
	#stack.send_message_over_gpio("hello world")
	stack.listen_for_input()

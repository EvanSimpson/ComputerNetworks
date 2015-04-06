import sys
import socket
import json
from bj import *
from UDP import UDP, UDPHeader, encode_udp, decode_udp
from datalink import Mac, encode_message, decode_message
from morse import morse_down, morse_up

localhost = '127.0.0.1'
routerport = 5073
gpioports = [5003, 5004, 5005]

LANs = {
			"A" : "127.0.0.1",
			"B" : "127.0.0.1",
			"C" : "127.0.0.1",
			"D" : "127.0.0.1"
			}

class RouterStack():

	def __init__(self):
		self.setup_bj()
		self.setup_servers()

	#setup functions

	def setup_bj(self):
		morse_layer = BJ(morse_down, morse_up)
		mac_layer = BJ(encode_message, decode_message)
		udp_layer = BJ(encode_udp, decode_udp)

		self.stack = BJ_Stack([udp_layer, mac_layer, morse_layer])
		self.extern_stack = BJ_Stack([udp_layer])

	def setup_servers(self):
		self.switch_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.switch_socket.bind((localhost, routerport))

		self.gpio_sockets = []

		for i in (range(len(gpioports)):
			self.gpio_sockets[i] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.gpio_sockets[i].sendto(bytearray(0x01), (localhost, gpioports[i]))

	#listening out over joesocket and gpio

	def listen_for_input(self):
		while True:
			try:
				self.listen_over_gpio()
			except:
				for socket in self.gpio_sockets:
					socket.close()
				sys.exit()

	def listen_over_gpio(self):
		for socket in self.gpio_sockets:
			(incoming, gpio_server_address) = socket.recvfrom(1024)
		self.handle_input_from_gpio(incoming, gpio_server_address)

	#handling inputs

	def handle_input_from_gpio(self, message_received, incoming_address):
		udp_input = self.stack.ascend(message_received)
		destination_port = udp_input.udp_header._destinationPort

		# decide which LAN this message is going to
		# if it's local, send it out over the appropriate socket
		# it it's another LAN, send it to the switch,
		# but what do we send the switch?
		dest_addr = udp_input.ip_header._destinationAddress
		dest_lan = dest_addr[0]
		if dest_lan == "C":
			# Going to stay internal to this LAN
			dest_client = dest_addr[1]

		else:
			# Needs to go out over the switch
			dest_lan_ip = LANs[dest_lan]
			to_send = self.extern_stack.descend(udp_input.packet)
			self.switch_socket.sendto(bytearray(to_send, encoding="UTF-8"), (dest_lan_ip, routerport))


		payload = udp_input.udp_header._payload
		source = (udp_input.ip_header._sourceAddress, udp_input.udp_header._sourcePort)


	# functions called on joesocket commands

	def joesocket_bind(self, source_address):
		port = source_address[1]
		self.send_acknowledgement(self.active_game_ports[port])

	def joesocket_close(self, source_address):
		port = source_address[1]
		if port in self.active_game_ports:
			socket_port = self.active_game_ports.pop(port)
		self.send_acknowledgement(socket_port)

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
		self.gpio_server_socket.sendto(to_transmit, self.gpio_address)

	def initialize_udp(self, source_address, destination_address, message_to_send):
		udp_header = UDPHeader()
		udp_header.setFields(source_address[1], destination_address[1], bytearray(message_to_send, encoding="UTF-8"))
		return UDP(udp_header, srcAddr=source_address[0], destAddr=destination_address[0])

if __name__ == "__main__":
	stack = Stack()
	stack.send_message_over_gpio("hello world")
	stack.listen_for_input()

import sys
import socket
import json
from bj import *
from UDP import UDP, UDPHeader, encode_udp, decode_udp
from datalink import Mac, encode_message, decode_message
from morse import morse_down, morse_up

localhost = '127.0.0.1'
routerport = 5073
local_lan = "C"
gpioports = {
	"1" : 5003, 
	"2" : 5004,
	"3" : 5005
	}

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

		self.internal_stack = BJ_Stack([mac_layer, morse_layer])
		self.external_stack = BJ_Stack([udp_layer])

	def setup_servers(self):
		self.switch_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.switch_socket.bind((localhost, routerport))

		self.gpio_sockets = {}

		for client_id in gpioports:
			self.gpio_sockets[client_id] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.gpio_sockets[client_id].sendto(bytearray(0x01), (localhost, gpioports[client_id]))

	#listening for input over switch and gpio

	def receive_input(self):
		while True:
			self.receive_over_gpio()
			self.receive_over_switch()

	def receive_over_switch():
		try:
			(incoming, socket_server_address) = switch_socket.recvfrom(1024)
			self.handle_input_from_switch(incoming, socket_server_address)
		except:
			switch_socket.close()
			sys.exit()

	def receive_over_gpio(self):
		#DO WE WANT TO CLOSE ALL OF THE SOCKETS BEFORE WE SYS.EXIT?
		try:
			for socket in self.gpio_sockets:
				(incoming, gpio_server_address) = socket.recvfrom(1024)
				self.handle_input_from_gpio(incoming, gpio_server_address)
		except:
			for socket in self.gpio_sockets:
				socket.close()
				sys.exit()
	
	#handling inputs

	def handle_input_from_switch(self, message_received, incoming_address):
		dummy_mac = Mac("0", "0", "0", message_received.decode("UTF-8"))
		
		udp_input = self.external_stack.ascend(dummy_mac)
		self.route_message(udp_input)

	def handle_input_from_gpio(self, message_received, incoming_address):
		mac_obj = self.internal_stack.ascend(message_received.decode("UTF-8"))
		self.route_message()

	def route_message(self, udp_input):
		# decide which LAN this message is going to
		# if it's local, send it out over the appropriate socket
		# it it's another LAN, send it to the switch
		
		if mac_obj.destination in gpioports:
			self.send_message_internally(mac_obj)
		else:
			udp_input = self.external_stack.ascend(mac_obj)
			self.send_message_externally(udp_input)

	def send_message_internally(self, mac_obj): 
		#send the message over the gpio to the pi corresponding with dest_client
		destination_client = mac_obj.destination

		port = gpioports[destination_client]
		gpio_socket = self.gpio_sockets[destination_client]
		message_in_bin = self.internal_stack.descend(mac_obj)
		#does the socket want a bytearray or a string?
		gpio_socket.sendto(bytearray(message_in_bin, encoding="UTF-8"), (localhost, port))

	def send_message_externally(self, udp_input):
		destination_lan_ip = LANs[udp_input.ip_header._destinationAddress[0]]

		serialized_udp_packet = self.external_stack.descend(udp_input)
		#to_send should be a bytearray but I'm not suuure
		self.switch_socket.sendto(serialized_udp_packet, (destination_lan_ip, routerport))
	
if __name__ == "__main__":
	print("nothing yet")

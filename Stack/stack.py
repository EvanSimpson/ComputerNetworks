import sys
import socket
import json
from bj import *
from UDP import encode_udp, decode_udp, encode_ip, decode_ip
from MAC import encode_mac, decode_mac
from datalink import Mac, encode_message, decode_message
from morse import morse_down, morse_up

localhost = '127.0.0.1'
routerport = 2048
ownport = 5000
authorityport = 5002
gpioport = 5003
local_lan = "C"
router_mac = "0"
local_mac_addresses = {
	"C0" : "0",
	"C1" : "X",
	"C2" : "Y",
	"C3" : "Z"
}

LANs = {
	"A" : "127.0.0.1",
	"B" : "127.0.0.1",
	"C" : "127.0.0.1",
	"D" : "127.0.0.1"
}

class Stack():

	def __init__(self, mac_address, is_router=False):
		self.mac_address = mac_address # Temporary - this should be loaded from a config file
		self.is_router = is_router
		self.active_game_ports = {}
		self.joesocket_commands = {
			"bind": self.joesocket_bind,
			"close": self.joesocket_close,
			"sendto": self.joesocket_sendto
		}

		self.setup_bj()
		self.setup_servers()

	#setup functions

	def setup_bj(self):
		morse_layer = BJ(morse_down, morse_up)
		mac_layer = BJ(encode_mac, decode_mac)
		ip_layer = BJ(encode_ip, decode_ip)
		udp_layer = BJ(encode_udp, decode_udp)

		self.internal_stack = BJ_Stack([mac_layer, morse_layer])
		self.external_stack = BJ_Stack([udp_layer, ip_layer])
		self.full_stack = BJ_Stack([udp_layer, ip_layer, mac_layer, morse_layer])

	def setup_servers(self):
		self.gpio_address = (localhost, gpioport)
		self.stack_address = (localhost, ownport)
		self.switch_address = (localhost, routerport)

		# Sockets need .setblocking(False) to prevent .recvfrom()
		# from blocking other socking from being read
		# while waiting for data to come in on whichever socket
		# is currently listening
		if self.is_router:
			self.switch_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.switch_socket.setblocking(False)
			self.switch_socket.bind(self.switch_address)
		else:
			self.game_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.game_server_socket.setblocking(False)
			self.game_server_socket.bind(self.stack_address)

		self.gpio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.gpio_server_socket.setblocking(False)
		self.gpio_server_socket.sendto(bytearray(0x01), self.gpio_address)

	#listening for input over switch and gpio

	def receive_input(self):
		while True:
			self.receive_over_gpio()
			if self.is_router:
				self.receive_over_switch()
			else:
				self.receive_from_games()

	def receive_from_games(self):
		try:
			(input_from_client, client_address) = self.game_server_socket.recvfrom(1024)
			print("input from client: " + str(input_from_client))
			self.handle_input_from_client(input_from_client, client_address)
		except KeyboardInterrupt:
			self.gpio_server_socket.close()
			self.game_server_socket.close()
			sys.exit()
		except socket.timeout as e:
			# Because of the non-blocking sockets, we need to catch
			# this extra timeout error. We're not always receiving data,
			# so a timeout isn't a bad thing, and like, we've got other
			# sockets to read!
			err = e.args[0]
			if err == 'timed out':
				pass
			else:
				print(e)
				sys.exit(1)
		except:
			pass

	def receive_over_switch(self):
		try:
			(incoming, socket_server_address) = self.switch_socket.recvfrom(1024)
			self.handle_input_from_switch(incoming, socket_server_address)
		except KeyboardInterrupt:
			self.gpio_server_socket.close()
			self.switch_socket.close()
			sys.exit()
		except socket.timeout as e:
			err = e.args[0]
			if err == 'timed out':
				pass
			else:
				print(e)
				sys.exit(1)
		except:
			pass

	def receive_over_gpio(self):
		try:
			(incoming, gpio_address) = self.gpio_server_socket.recvfrom(1024)
			print("incoming: " + str(incoming))
			self.handle_input_from_gpio(incoming, gpio_address)
		except KeyboardInterrupt:
			self.gpio_server_socket.close()
			if self.is_router:
				self.switch_socket.close()
			else:
				self.game_server_socket.close()
			sys.exit(1)
		except socket.timeout as e:
			err = e.args[0]
			if err == 'timed out':
				pass
			else:
				print(e)
				sys.exit(1)
		except:
			pass

	#handling inputs

	def handle_input_from_switch(self, message_received, incoming_address):
		print("got message over switch")
		print(message_received.decode("UTF-8"))
		dummy_mac = Mac("0", "0", "0", message_received.decode("UTF-8"))

		udp_input = self.external_stack.ascend(dummy_mac)
		self.send_message_internally(udp_input)

	def handle_input_from_client(self, message_bytearray, client_address):
		print(str(message_bytearray))
		parsed_message = json.loads(message_bytearray.decode("UTF-8"))
		if parsed_message['params']['source_address'][1] not in self.active_game_ports:
			self.add_new_client(parsed_message['params']['source_address'][1], client_address)

		self.joesocket_commands[parsed_message['command']](**parsed_message['params'])

	def add_new_client(self, port_letter, client_address):
		self.active_game_ports[port_letter] = client_address

	def handle_input_from_gpio(self, message_received, incoming_address):
		print("in handle input from gpio")
		print("message received: " + str(message_received))
		mac_payload = self.internal_stack.ascend(message_received.decode("UTF-8"))
		print("mac payload: " + str(mac_payload))
		print("mac_payload dest is " + str(mac_payload.dest))
		print("mac address is " + str(mac_address))
		if self.is_router:
			self.route_message(mac_payload)
		elif mac_payload.dest == self.mac_address:
			print("about to ascend stack")
			udp_input = self.full_stack.ascend(message_received.decode("UTF-8"))
			print("udp input is : " + str(udp_input))
			self.send_message_to_application(udp_input)

	def send_message_to_application(self, udp_input):
		# udp_input = (srcPort, srcLan, srcHost, destPort, destLan, destHost, payload)
		print("in send message to application")
		destination_port = udp_input[3]
		print("destination port is " + str(destination_port))
		print("active game ports: " + str(active_game_ports))
		if destination_port in self.active_game_ports:
			destination_address = self.active_game_ports[destination_port]
			print("destination address is: " + str(destination_address))
			payload = udp_input[6]
			source = (udp_input[1]+udp_input[2], udp_input[0])

			to_send = json.dumps([{'payload': payload, 'address': source}])
			print("to send is " + str(to_send))
			try:
				print("about to send to game_server_socket: " + str(destination_address))
				game_server_socket.sendto(to_send, destination_address)

			except:
				pass

	def route_message(self, mac_obj):
		# check the mac address, if it is for the router
		# then take it up the stack and figure out
		# if it is for out lan and if so, what the IP is
		# then recreate the packet with the proper ip
		# and send it to the
		print("in route message")
		print("mac destination is " + mac_obj.dest)
		udp_obj = self.external_stack.ascend(mac_obj)
		if mac_obj.dest == "0":
			print("mac destination is router")
			self.send_message_externally(udp_obj)

	def send_message_internally(self, udp_input):
		#send the message over the gpio to the pi corresponding with dest_client
		print("in send message internally")
		destination_host_ip = udp_input[4] + udp_input[5]
		print("destination host ip is " + destination_host_ip)
		destination_mac_address = local_mac_addresses[destination_host_ip]

		if udp_input[1] is local_lan:
			source_host_ip = udp_input[2]
			source_mac_address = local_mac_addresses[local_lan+source_host_ip]
		else:
			source_mac_address = self.mac_address # the router's MAC address
		print("source address: "+ source_mac_address)
		print("dest address: " + destination_mac_address)
		#does the socket want a bytearray or a string?
		print(udp_input[6])
		self.send_message_over_gpio(( udp_input[1]+udp_input[2], udp_input[0]), ( udp_input[4]+udp_input[5], udp_input[3]), udp_input[6])

	def send_message_externally(self, udp_input):
		destination_lan_ip = LANs[udp_input.ip_header._destinationAddress[0]]

		serialized_udp_packet = self.external_stack.descend(udp_input)
		#to_send should be a bytearray but I'm not suuure
		try:
			self.switch_socket.sendto(serialized_udp_packet, (destination_lan_ip, routerport))
		except:
			pass

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
		print("in send to: " + str(data))
		self.send_message_over_gpio(source_address, destination_address, data)
		self.send_acknowledgement(self.active_game_ports[source_address[1]])

	def send_acknowledgement(self, client_address):
		return_message = bytearray(json.dumps({"Error": 0}), encoding="UTF-8")
		try:
			self.game_server_socket.sendto(return_message, client_address)
		except:
			pass

	#sending data over gpio based on input from joesocket

	def send_message_over_gpio(self, source_address, destination_address, message_to_send):
		# address = (LAN+host, port)
		# param_tuple = (srcPort, srcLan, srcHost, destPort, destLan, destHost, payload)
		stack_entry = (source_address[1], source_address[0][0], source_address[0][1], str(destination_address[1]), destination_address[0][0], destination_address[0][1], message_to_send)
		to_transmit_string = self.full_stack.descend(stack_entry)
		to_transmit = bytearray(to_transmit_string, encoding='UTF-8')
		print("to transmit: " + to_transmit_string)
		try:
			print("about to send the message")
			self.gpio_server_socket.sendto(to_transmit, self.gpio_address)
		except:
			pass

if __name__ == "__main__":
	message = bytearray("111010101110001110101110111000111010111010001011101110111011100011101011101000101011101110111000101110001110111011101110111000101110111011101110001010111011101110001011100010101011101110001010101011100010101011101110001010101011100010101010001010000000", encoding="UTF-8")
	stack = Stack(is_router=True)
	stack.receive_input()
	# stack.handle_input_from_gpio(message, ("C1"))

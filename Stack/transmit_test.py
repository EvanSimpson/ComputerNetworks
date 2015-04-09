import pi
from bj import *
from UDP import UDP, UDPHeader, encode_udp, decode_udp
from datalink import Mac, encode_message, decode_message
from morse import morse_down, morse_up
import socket

if __name__ == "__main__":
	morse_layer = BJ(morse_down, morse_up)
	mac_layer = BJ(encode_message, decode_message)
	udp_layer = BJ(encode_udp, decode_udp)

	stack = BJ_Stack([udp_layer, mac_layer, morse_layer])

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def send(raw_data):
		data = raw_data.upper()
		if data.isalnum():
			udp_header = UDPHeader()
			udp_header.setFields('01', '02', bytearray(data, encoding="UTF-8"))
			udp_obj = UDP(udp_header, srcAddr='A', destAddr='C')
			data = stack.descend(udp_obj)
			#print(data)
			sock.sendto(bytearray(data, encoding="UTF-8"), ('127.0.0.1', 5003))
			#pi.transmit(data, 18, 23)
	while True:
		try:
			s = input('--> ')
			send(s)
		except KeyboardInterrupt:
			break

	sock.close()
	pi.kill()

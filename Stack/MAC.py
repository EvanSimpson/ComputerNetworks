MAC_TABLE = {
	"C1" : "X",
	"C2" : "Y",
	"C3" : "Z"
}

def encode_mac(param_tuple):
	# (src_ip, dest_ip, ip_packet)
	src_mac = MAC_TABLE.get(param_tuple[0], "0")
	dest_mac = MAC_TABLE.get(param_tuple[1], "0")
	
	mac_obj = MAC(param_tuple[0], param_tuple[1], param_tuple[2])
	return mac_obj.packet

def decode_mac(packet):
	mac_obj = MAC(packet)
	# (srcLan, srcHost, destLan, destHost, packet)
	return mac_obj

class MAC(object):
	def __init__(self, src, dest=False, payload=False):
		if dest:
			self.src = src
			self.dest = dest
			self.payload = payload
			self.packet = src+dest+payload
		else:
			self.parse(src)

	def parse(self, packet):
		self.packet = packet
		self.src = packet[0:2]
		self.dest = packet[2:4]
		self.payload = packet[4:]


if __name__ == "__main__":
	from UDP import encode_udp, decode_udp, encode_ip, decode_ip

	packet = encode_mac(encode_ip(encode_udp(("01", "C", "1", "01", "C", "2", "HELLO"))))
	print(packet)
	info = decode_udp(decode_ip(decode_mac(packet)))
	print(info)
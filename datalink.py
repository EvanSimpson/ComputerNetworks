addresses = ['A', 'B', 'C', 'D']
protocols = ['NETWORK']

class MacHeader():

	def __init__(self, destination, source, next_protocol, payload):
		'''
		Takes as input strings for each value of the 
		'''
		self.destination = destination
		self.source = source
		self.next_protocol = next_protocol
		self.payload = payload

	def verify(self):
		if not self.destination in addresses: 
			raise ValueError("That is not a valid destination.")
		if not self.source in addresses:
			raise ValueError("This is not a valid source.")
		if not self.next_protocol in protocols:
			raise ValueError("That is not a valid next protocol code.")

	def create_header(self):
		self.verify()
		return self.destination + self.source + self.next_protocol + self.payload + self.create_checksum()

	def create_checksum(self):
		'''
		this creates the crc 
		'''
		return "checksum"

def encode_mac_header(mac_header_obj):
	return mac_header_obj.create_header()

def decode_mac_header(mac_header_text):
	'''
	convert the mac header string into a mac header object 
	'''
	return



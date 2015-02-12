class MacHeader():

	def __init__(self, destination, source, next_protocol, payload):
		'''
		Takes as input strings for each value of the 
		'''
		self.destination = destination
		self.source = source
		self.next_protocol = next_protocol
		self.payload = payload

	def create_header(self):
		return self.destination + self.source + self.next_protocol + self.payload + self.create_checksum()

	def create_checksum(self):
		'''
		
		'''

def encode_mac_header(mac_header_obj):

	return mac_header_obj.create_header()




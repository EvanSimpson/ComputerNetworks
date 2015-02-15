addresses = ['A', 'B', 'C', 'D']
protocols = ['NET']

class Mac():

	def __init__(self, destination, source, next_protocol, payload):
		'''
		Takes as input strings for each value of the 
		'''
		self.destination = destination
		self.source = source
		self.next_protocol = next_protocol
		self.payload = payload
		self.verify_arguments()

	def verify_arguments(self):
		if not self.destination in addresses: 
			raise ValueError("That is not a valid destination.")
		if not self.source in addresses:
			raise ValueError("This is not a valid source.")
		if not self.next_protocol in protocols:
			raise ValueError("That is not a valid next protocol code.")

	def create_message(self):
		'''
		outputs the parts (header and payload) concatonated into a string in 
		the order: destination, source, next protocol, payload, checksum
		'''
		return self.destination + self.source + self.next_protocol + self.payload + self.create_message_checksum()

	def verify(self, parsed_payload, parsed_checksum):
		'''
		uses the checksum to make sure the proper message was received and decoded
		'''
		return True #self.generate_checksum_value(parsed_payload+parsed_checksum) == 0

	def create_message_checksum(self):
		'''
		creates string version of the crc and outputs the checksum value as a string 
		'''
		return self.generate_checksum_value(self.payload) #.toString()

	def generate_checksum_value(self, payload):
		'''
		does all the fancy stuff maor and evan are writing 
		'''
		return ""

def encode_message(mac_obj):
	'''
	creates a mac string out of a existing mac object that contains all of the parts needed for the message
	'''
	return mac_obj.create_message()

def decode_message(mac_text):
	'''
	convert the mac object string into a mac object 
	'''
	destination = mac_text[0]
	source = mac_text[1]
	next_protocol = mac_text[2:5]
	payload = mac_text[5:len(mac_text)-2]
	checksum = mac_text[len(mac_text)-2]
	
	mac_obj = Mac(destination, source, next_protocol, payload)

	if mac_obj.verify(payload, checksum):
		return mac_obj
	else:
		return "NO"



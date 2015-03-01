#from crc import crc
addresses = [ord('A'), ord('B'), ord('C'), ord('D')]
protocols = [ord('N')]

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

	def __str__(self):
		to_string = "[ Destinstion: " + chr(self.destination) + ", Source: " + chr(self.source) +", Next Protocol: " + chr(self.next_protocol) +", Payload: " + str(self.payload) + " ]"
		return to_string
		
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
		return bytearray([
			self.destination >> 8,
			self.destination & 0xFF,
			self.source >> 8,
			self.source & 0xFF,
			self.next_protocol >> 8,
			self.next_protocol & 0xFF,
			]) + self.payload

	def payload_to_binary(self):
		'''
		turns the payload into a binary string
		'''
		return ''.join(['%08d'%int(bin(ord(i))[2:]) for i in self.payload])

def encode_message(mac_obj):
	'''
	creates a mac string out of a existing mac object that contains all of the parts needed for the message
	'''
	return mac_obj.create_message()

def decode_message(mac_bytearray):
	'''
	converts the mac object string into a mac object, 
	verifies that the payload has been properly transmitted, 
	and outputs the verified mac object
	'''

	destination = mac_bytearray[0]
	source = mac_bytearray[1] 
	next_protocol = mac_bytearray[2]
	payload = mac_bytearray[3:]

	return Mac(destination, source, next_protocol, payload)

if __name__ == "__main__":

	mo = Mac(ord('A'), ord('B'), ord("N"), bytearray("HELLO", encoding = "UTF-8"))	
	encode_message(mo)
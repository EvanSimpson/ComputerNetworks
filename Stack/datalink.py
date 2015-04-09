from crc import crc
addresses = ["A", "B", "C", "D"]
protocols = [1]

class Mac():

	def __init__(self, destination, source, next_protocol, payload):
		'''
		Takes as input strings for each value of the
		'''
		self.destination = destination if type(destination) is bytearray else bytearray(destination, encoding="UTF-8")
		self.source = source if type(source) is bytearray else bytearray(source, encoding="UTF-8")
		self.next_protocol = next_protocol if type(next_protocol) is bytearray else bytearray(next_protocol, encoding="UTF-8")
		self.payload = payload
		self.calculate_checksum()
		#self.verify_arguments()

	def __str__(self):
		to_string = "[ Destination: " + str(self.destination) + ", Source: " + str(self.source) +", Next Protocol: " + str(self.next_protocol) +", Payload: " + str(self.payload) + " ]"
		return to_string

	def verify_arguments(self):
		if not self.destination in addresses and not chr(self.destination) in addresses:
			raise ValueError(str(self.destination) + " is not a valid destination.")
		if not self.source in addresses and not chr(self.destination) in addresses:
			raise ValueError(str(self.source) + " is not a valid source.")
		if not self.next_protocol in protocols:
			raise ValueError(str(self.next_protocol) + " is not a valid next protocol code.")

	def calculate_checksum(self):
		self.checksum = crc(self.destination + self.source + self.next_protocol + self.payload)

	def create_message(self):
		'''
		outputs the parts (header and payload) concatonated into a string in
		the order: destination, source, next protocol, payload, checksum
		'''

		return self.destination + self.source + self.next_protocol + self.payload + self.checksum

	def payload_to_binary(self):
		'''
		turns the payload into a binary string
		'''
		return ''.join(['%08d'%int(bin(ord(i))[2:]) for i in self.payload])

def encode_message(message):
	'''
	creates a mac string out of a existing mac object that contains all of the parts needed for the message
	'''
	if type(message) is bytearray:
		mac_obj = Mac("0", "0", '0', message)
	else:
		mac_obj = message
	return mac_obj.create_message()

def decode_message(mac_bytearray):
	'''
	converts the mac object string into a mac object,
	verifies that the payload has been properly transmitted,
	and outputs the verified mac object
	'''
	destination = mac_bytearray[0:1]
	source = mac_bytearray[1:2]
	next_protocol = mac_bytearray[2:3]
	payload = mac_bytearray[3:len(mac_bytearray) - 2]
	checksum = mac_bytearray[-2:]

	mac_obj = Mac(destination, source, next_protocol, payload)
	return mac_obj

if __name__ == "__main__":

	mo = Mac(ord('A'), ord('B'), ord("N"), bytearray("HELLO", encoding = "UTF-8"))
	encode_message(mo)

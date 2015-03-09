from datalink import Mac, encode_message, decode_message
from physical import physical_down, physical_up
from UDP import UDP, Layer4, encode_udp, decode_udp
	
class BJ_Stack():
	def __init__(self, bjs):
		self._descend = tuple(bjs)
		bjs.reverse()
		self._ascend = tuple(bjs)

	def ascend(self, message):
		'''
			ascend the stack
		'''
		return self.up_step(self._ascend, message)

	def descend(self, message):
		'''
			descend the stack
		'''
		return self.down_step(self._descend, message)

	def up_step(self, stack, message):
		'''
			port the message up one level
		'''
		if len(stack) == 0:
			return message
		# Call the next step with message as one stack up
		return self.up_step(stack[1:], stack[0].inv(message))

	def down_step(self, stack, message):
		'''
			port the message down one level
		'''
		if len(stack) == 0:
			return message
		# Call the next step with message as one stack up
		return self.down_step(stack[1:], stack[0](message))



class BJ():
	def __init__(self, down_func, up_func):
		self._turn_down = down_func
		self._turn_up = up_func

	def __call__(self, for_what):
		'''
		for_what = the message in its current state
		'''
		return self._turn_down(for_what)

	def inv(self, for_what):
		'''
		for_what = the message in its current state
		'''
		return self._turn_up(for_what)

if __name__ == "__main__":
	'''
		main function to transmit up/down the stack
	'''
	def forward(argument):
		return argument - 1

	def backward(argument):
		return argument + 1

	#mac = Mac(ord('A'), ord('B'), 1, bytearray("HELLO", encoding="UTF-8"))	
	
	layer4 = Layer4()
	layer4.setFields(1, 2, bytearray('AD0011PAYLOAD', encoding='UTF-8'))
	udp_obj = UDP(layer4, ord("C"), ord("D")) #should these be 2 characters?
	
	mac_layer = BJ(encode_message, decode_message)
	physical_layer = BJ(physical_down, physical_up)
	udp_layer = BJ(encode_udp, decode_udp)
	
	stack = BJ_Stack([udp_layer, mac_layer, physical_layer])

	print(stack.ascend(stack.descend(udp_obj)))

from stack import Stack

def test_as_host():
	stack = Stack()

	source_address = ("C1", "34")
	destination_address =  ("C2", "34")
	
	while True:
		message = input("type a message (type q to quit): ")
		if message == "q":
			break
		#print(message)
		stack.send_message_over_gpio(source_address, destination_address, message)

if __name__ == "__main__":
	test_as_host()
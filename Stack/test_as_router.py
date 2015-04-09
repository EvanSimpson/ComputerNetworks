from stack import Stack

def test_as_router():
	stack = Stack(is_router=True)
	while True:
		stack.receive_over_gpio()

if __name__ == "__main__":
	test_as_router()
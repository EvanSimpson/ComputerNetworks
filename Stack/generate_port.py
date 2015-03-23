import sys

current_port_nums = []

def generate_port_num():
	while True:
		if sys.stdin.readline() == "1":
			if current_port_nums[-1] > 99:
				for i in range(100):
					if i not in current_port_nums:
						current_port_nums.append(i)
						current_port_nums.sort()
						yield i
						break
			else:
				yield current_port_nums[-1] + 1


if __name__ == "__main__":
	generate_port_num()
def checksum(header):
	header_sum = sum(header)
	hex_header = hex(header_sum)[2:]
	length = len(hex_header)
	while (length>4):
		core = hex_header[length-4:]
		carry = hex_header[:length-4]
		out = int(carry,16) + int(core,16)
		hex_header = hex(out)[2:]
		length = len(hex_header)

	hex_header = '0'*(4 - length) + hex_header
	return bytearray(hex_header, encoding="utf-8")


if __name__ == "__main__":
	x = bytearray('BAAD0010', encoding="utf-8")
	print(checksum(x))

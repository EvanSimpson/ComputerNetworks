def crc(data_ba,key='101010101'):
    """Input data and key a as binary lists"""
    data_dec = sum(data_ba)
    data = bin(data_dec) #Converts data to a binary string
    L = len(key)
    data = data + '0'*(L-1)

    while (True):
        x = data[0:L]
        y = bin(int(x,2) ^ int(key,2))
        y = y[2:]
        data = y + data[L:]
        if len(data)<L:
            break

    y = hex(int(y,2))
    y = y[2:]
    y = '0'*(2 - len(y)) + y
    return bytearray(y, encoding="UTF-8")



if __name__ == '__main__':
    print(crc(bytearray('abcdefgh', encoding="UTF-8")))

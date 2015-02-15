

def crc(data,key='101010101'):
    """Input data and key a as binary lists"""
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
    return y
    


if __name__ == '__main__':
     print crc('1101110110010101010101')
     
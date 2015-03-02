def byteArrayToInt(data):
    length = len(data)
    val = 0
    for i in range(length):
        val |= data[length-(i+1)] << (i*8)
    return val

class Layer3(object):
    def __init__(self):
        pass

    def setFields(self, srcAddr, destAddr, protocol, udpPacket):
        self._sourceAddress = srcAddr
        self._destinationAddress = destAddr
        self._nextProtocol = protocol
        self._payloadLength = len(udpPacket)

    def serialize(self):
        header = bytearray([
            (self._sourceAddress >> 24) & 0xFF,
            (self._sourceAddress >> 16) & 0xFF,
            (self._sourceAddress >> 8) & 0xFF,
            self._sourceAddress & 0xFF,
            (self._destinationAddress >> 24) & 0xFF,
            (self._destinationAddress >> 16) & 0xFF,
            (self._destinationAddress >> 8) & 0xFF,
            self._destinationAddress & 0xFF,
            0x00,
            self._nextProtocol & 0xFF,
            (self._payloadLength >> 8) & 0xFF,
            self._payloadLength & 0xFF
        ])
        return header

    def parseFields(self, data):
        # why are these addresses so long
        self._sourceAddress = byteArrayToInt(data[0:4])
        self._destinationAddress = byteArrayToInt(data[4:8])
        self._nextProtocol = data[9]
        self._payloadLength = byteArrayToInt(data[10:])

class Layer4(object):
    def __init__(self):
        pass

    def calculateChecksum(self):
        '''
            Use stored data fields to calculate the packet checksum
        '''
        self._checksum = 0xFFFF

    def setFields(self, sPort, dPort, payload):
        '''
            sPort is expected to be an integer
            dPort is expected to be an integer
            paylaod is expected to be a bytearray
        '''
        self._sourcePort = sPort
        self._destinationPort = dPort
        self._length = len(payload)
        self._payload = payload
        self.calculateChecksum()

    def serialize(self):
        '''
            Serialize the stored fields into a bytearray packet
            to be passed down the stack
        '''
        packet = bytearray([
            self._sourcePort >> 8,
            self._sourcePort & 0xFF,
            self._destinationPort >> 8,
            self._destinationPort & 0xFF,
            self._length >> 8,
            self._length & 0xFF,
            self._checksum >> 8,
            self._checksum & 0xFF
            ]) + self._payload
        return packet

    def parseFields(self, data):
        '''
            Data is a bytearray of the entire incoming UDP packet
        '''
        self._sourcePort = byteArrayToInt(data[0:2])
        self._destinationPort = byteArrayToInt(data[2:4])
        self._length = byteArrayToInt(data[4:6])
        self._checksum = byteArrayToInt(data[6:8])
        self._payload = data[8:]

        if not len(self._payload) == self._length:
            print("Error! Lengths don't match")


if __name__ == "__main__":
    udp = Layer4()
    udp.setFields(1, 2, bytearray('hello there', 'UTF-8'))
    print(udp.serialize())
    udp.parseFields(udp.serialize())
    print(udp.serialize())

    header = Layer3()
    header.setFields(ord('A'), ord('B'), 2, udp.serialize())
    print(header.serialize())
    header.parseFields(header.serialize())
    print(header.serialize())

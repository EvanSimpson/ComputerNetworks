from datalink import Mac

def byteArrayToInt(data):
    length = len(data)
    val = 0
    for i in range(length):
        val |= data[length-(i+1)] << (i*8)
    return val

def encode_udp(udp_obj):
    return udp_obj.layer3.serialize()

def decode_udp(mac_obj): #change this to be a mac object not a bytearray
    header = Layer3()
    header.parseFields(mac_obj)

    packetObj = Layer4()
    packetObj.parseFields(header._payload)

    return packetObj._payload

class UDP(object):

    def __init__(self, layer4, srcAddr, destAddr):
        self.layer4 = layer4
        self.packet = self.layer4.serialize()

        self.layer3 = Layer3()
        self.layer3.setFields(srcAddr, destAddr, 1, self.packet)

class Layer3(object):
    def __init__(self):
        pass

    def setFields(self, srcAddr, destAddr, protocol, udpPacket):
        self._sourceAddress = srcAddr
        self._destinationAddress = destAddr
        self._nextProtocol = protocol
        self._payloadLength = len(udpPacket)
        self._payload = udpPacket

    def serialize(self):
        # packet = bytearray([
        #     (self._sourceAddress >> 24) & 0xFF,
        #     (self._sourceAddress >> 16) & 0xFF,
        #     (self._sourceAddress >> 8) & 0xFF,
        #     self._sourceAddress & 0xFF,
        #     (self._destinationAddress >> 24) & 0xFF,
        #     (self._destinationAddress >> 16) & 0xFF,
        #     (self._destinationAddress >> 8) & 0xFF,
        #     self._destinationAddress & 0xFF,
        #     0x00,
        #     self._nextProtocol & 0xFF,
        #     (self._payloadLength >> 8) & 0xFF,
        #     self._payloadLength & 0xFF
        # ]) + self._payload
        return Mac(self._destinationAddress, self._sourceAddress, self._nextProtocol, self._payload)

    def parseFields(self, mac_obj):
        # why are these addresses so long
        self._sourceAddress = mac_obj.source #byteArrayToInt(data[0:4])
        self._destinationAddress = mac_obj.destination #byteArrayToInt(data[4:8])
        self._nextProtocol = mac_obj.next_protocol #data[9]
        self._payloadLength = byteArrayToInt(mac_obj.payload) #byteArrayToInt(data[10:12])
        self._payload = mac_obj.payload

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
        print()
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
    header.setFields(ord('A'), ord('B'), 1, udp.serialize())
    print(header.serialize())
    header.parseFields(header.serialize())
    print(header.serialize())

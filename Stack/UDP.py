from datalink import Mac

def byteArrayToInt(data):
    length = len(data)
    val = 0
    for i in range(length):
        val |= data[length-(i+1)] << (i*8)
    return val

def encode_udp(udp_obj):
    print("in encode udp")
    return udp_obj.ip_header.serialize()

def decode_udp(mac_obj):
    print("in decode udp")
    ip_header = IPHeader()
    ip_header.parseFields(mac_obj)

    packetObj = UDPHeader()
    packetObj.parseFields(ip_header._payload)

    return packetObj._payload

class UDP(object):

    def __init__(self, udp_header, srcAddr, destAddr):
        self.udp_header = udp_header
        self.packet = self.udp_header.serialize()

        self.ip_header = IPHeader()
        self.ip_header.setFields(srcAddr, destAddr, '1', self.packet)

    def __str__(self):
        return "[ Destination Port: " + str(self.udp_header._destinationPort) + "," \
            "Source Port: " + str(self.udp_header._sourcePort) + "," \
            "UDP Header Payload Length: " + str(self.udp_header._length) + "," \
            "UDP Header Payload: " + str(self.udp_header._payload) + "," \
            "Source Address: " + str(self.ip_header._sourceAddress) + "," \
            "Destination Address: " + str(self.ip_header._destinationAddress) + "," \
            "IP Header Payload Length: " + str(self.ip_header._payloadLength) + "," \
            "IP Header Payload: " + str(self.ip_header._payload)

class IPHeader(object):
    def __init__(self):
        pass

    def setFields(self, srcAddr, destAddr, protocol, udpPacket):
        self._sourceAddress = bytearray(srcAddr, encoding="UTF-8")
        self._destinationAddress = bytearray(destAddr, encoding="UTF-8")
        self._nextProtocol = bytearray(protocol, encoding="UTF-8")
        self._payloadLength = bytearray(str(len(udpPacket)), encoding="UTF-8")
        self._payload = udpPacket

    def serialize(self):
        packet = self._sourceAddress + self._destinationAddress + self._nextProtocol + self._payloadLength + self._payload
        # bytearray([
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
        return packet

    def parseFields(self, mac_obj):
        # why are these addresses so long
        self._sourceAddress = mac_obj.payload[0:2] #byteArrayToInt(data[0:4])
        self._destinationAddress = mac_obj.payload[2:4] #byteArrayToInt(data[4:8])
        self._nextProtocol = mac_obj.payload[5] #data[9]
        self._payloadLength = byteArrayToInt(mac_obj.payload[5:]) #byteArrayToInt(data[10:12])
        self._payload = mac_obj.payload[5:]
        print("ip payload is " + str(self._payload))

class UDPHeader(object):
    def __init__(self):
        pass

    def calculateChecksum(self):
        '''
            Use stored data fields to calculate the packet checksum
        '''
        self._checksum = bytearray("XZ", encoding="UTF-8")#0xFFFF

    def setFields(self, sPort, dPort, payload):
        '''
            sPort is expected to be an integer
            dPort is expected to be an integer
            paylaod is expected to be a bytearray
        '''
        self._sourcePort = bytearray(sPort, encoding="UTF-8")
        self._destinationPort = bytearray(dPort, encoding="UTF-8")
        self._length = bytearray(str(len(payload)), encoding="UTF-8")
        self._payload = payload
        self.calculateChecksum()

    def serialize(self):
        '''
            Serialize the stored fields into a bytearray packet
            to be passed down the stack
        '''
        #packet = 
        # bytearray([
        #     self._sourcePort >> 8,
        #     self._sourcePort & 0xFF,
        #     self._destinationPort >> 8,
        #     self._destinationPort & 0xFF,
        #     self._length >> 8,
        #     self._length & 0xFF,
        #     self._checksum >> 8,
        #     self._checksum & 0xFF
        #     ]) + self._payload
        return self._sourcePort + self._destinationPort + self._length + self._checksum + self._payload

    def parseFields(self, data):
        '''
            Data is a bytearray of the entire incoming UDP packet
        '''
        self._sourcePort = byteArrayToInt(data[0:2])
        self._destinationPort = byteArrayToInt(data[2:4])
        self._length = data[4:6]
        self._checksum = byteArrayToInt(data[6:8])
        self._payload = data[8:]

        if not bytearray(str(len(self._payload)), encoding="UTF-8") == self._length:
            print("Error! Lengths don't match")


if __name__ == "__main__":
    udp = UDPHeader()
    udp.setFields(1, 2, bytearray('hello there', 'UTF-8'))
    print(udp.serialize())
    udp.parseFields(udp.serialize())
    print(udp.serialize())

    header = IPHeader()
    header.setFields(ord('A'), ord('B'), 1, udp.serialize())
    print(header.serialize())
    header.parseFields(header.serialize())
    print(header.serialize())

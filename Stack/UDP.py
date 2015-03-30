from datalink import Mac
from ipv4checksum import checksum

def byteArrayToInt(data):
    length = len(data)
    val = 0
    for i in range(length):
        val |= data[length-(i+1)] << (i*8)
    return val

def encode_udp(udp_obj):
    return udp_obj.ip_header.serialize()

def decode_udp(mac_obj):
    ip_header = IPHeader()
    ip_header.parseFields(mac_obj)

    udp_header = UDPHeader()
    udp_header.parseFields(ip_header._payload)

    udp_obj = UDP(udp_header, ip_header=ip_header)

    return udp_obj

class UDP(object):

    def __init__(self, udp_header, srcAddr=False, destAddr=False, ip_header=False):
        self.udp_header = udp_header
        self.packet = self.udp_header.serialize()

        if not srcAddr and not destAddr:
            self.ip_header = ip_header

        elif not ip_header:
            self.ip_header = IPHeader()
            self.ip_header.setFields(srcAddr, destAddr, '1', self.packet)

    def __str__(self):
        return "[ Destination Port: " + str(self.udp_header._destinationPort) + "," \
            "Source Port: " + str(self.udp_header._sourcePort) + "," \
            "UDP Header Payload Length: " + str(len(self.udp_header._payload)) + "," \
            "UDP Header Payload: " + str(self.udp_header._payload) + "," \
            "Source Address: " + str(self.ip_header._sourceAddress) + "," \
            "Destination Address: " + str(self.ip_header._destinationAddress) + "," \
            "IP Header Payload: " + str(self.ip_header._payload)

class IPHeader(object):
    def __init__(self):
        pass

    def setFields(self, srcAddr, destAddr, protocol, udpPacket):
        self._sourceAddress = bytearray(srcAddr, encoding="UTF-8")
        self._destinationAddress = bytearray(destAddr, encoding="UTF-8")
        self._nextProtocol = bytearray(protocol, encoding="UTF-8")
        self._checklessHeader = self._sourceAddress + self._destinationAddress + self._nextProtocol
        self._checksum = checksum(self._checklessHeader)
        self._payload = udpPacket

    def serialize(self):
        packet = self._sourceAddress + self._destinationAddress + self._nextProtocol + self._checksum + self._payload
        return packet

    def parseFields(self, mac_obj):
        # why are these addresses so long
        self._sourceAddress = mac_obj.payload[0:2]
        self._destinationAddress = mac_obj.payload[2:4]
        self._nextProtocol = mac_obj.payload[4]
        self._checksum = mac_obj.payload[5:9]
        self._payload = mac_obj.payload[9:]

class UDPHeader(object):
    def __init__(self):
        pass

    def setFields(self, sPort, dPort, payload):
        '''
            sPort is expected to be a string
            dPort is expected to be a string
            paylaod is expected to be a bytearray
        '''
        self._sourcePort = bytearray(sPort, encoding="UTF-8")
        self._destinationPort = bytearray(dPort, encoding="UTF-8")
        self._payload = payload

    def serialize(self):
        '''
            Serialize the stored fields into a bytearray packet
            to be passed down the stack
        '''
        return self._sourcePort + self._destinationPort + self._payload

    def parseFields(self, data):
        '''
            Data is a bytearray of the entire incoming UDP packet
        '''
        self._sourcePort = data[0:2]
        self._destinationPort = data[2:4]
        self._payload = data[4:]


if __name__ == "__main__":
    udp = UDPHeader()
    udp.setFields('01', '02', bytearray('hello there', 'UTF-8'))
    print(udp.serialize())
    udp.parseFields(udp.serialize())
    print(udp.serialize())

    header = IPHeader()
    header.setFields('AC', 'BD', '1', udp.serialize())
    print(header.serialize())

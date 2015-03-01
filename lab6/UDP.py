class UDP(object):
    def __init__(self):
        pass

    def calculateChecksum(self):
        self._checksum = 0xFF

    def setFields(self, sPort, dPort, payload):
        self._sourcePort = sPort
        self._destinationPort = dPort
        self._length = len(payload)
        self._payload = payload
        self.calculateChecksum()

    def serialize(self):
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
        self._sourcePort = (int(data[0]) << 8) | int(data[1])
        self._destinationPort = (int(data[2]) << 8) | int(data[3])
        self._length = (int(data[4]) << 8) | int(data[5])
        self._checksum = (int(data[6]) << 8) | int(data[7])
        self._payload = data[8:]

        print(self._length)

        if not len(self._payload) == self._length:
            print("Error! Lengths don't match")


if __name__ == "__main__":
    udp = UDP()
    udp.setFields(ord('A'), ord('B'), bytearray('hello', 'UTF-8'))
    print(udp.serialize())
    udp.parseFields(udp.serialize())
    print(udp.serialize())

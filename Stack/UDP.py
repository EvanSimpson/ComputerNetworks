from datalink import Mac
from ipv4checksum import checksum

def byteArrayToInt(data):
    length = len(data)
    val = 0
    for i in range(length):
        val |= data[length-(i+1)] << (i*8)
    return val

def encode_udp(param_tuple):
    # param_tuple = (srcPort, srcLan, srcHost, destPort, destLan, destHost, payload)
    udp_obj = UDP(param_tuple[0], destPort=param_tuple[3], payload=param_tuple[6])
    udp_packet = udp_obj.packet
    return (param_tuple[1], param_tuple[2], param_tuple[4], param_tuple[5], "A", udp_packet)

def decode_udp(param_tuple):
    # param_tuple = (srcLan, srcHost, destLan, destHost, packet)
    udp_obj = UDP(param_tuple[4])

    return (udp_obj.srcPort, param_tuple[0], param_tuple[1], udp_obj.destPort, param_tuple[2], param_tuple[3], udp_obj.payload)


def encode_ip(param_tuple):
    # param_tuple = (srcLan, srcHost, destLan, destHost, nextProtocol, payload)
    ip_obj = IP(param_tuple[0], param_tuple[1], param_tuple[2], param_tuple[3], param_tuple[4], param_tuple[5])

    return (ip_obj.srcLan+ip_obj.srcHost, ip_obj.destLan+ip_obj.destHost, ip_obj.packet)

def decode_ip(mac_obj):
    ip = IP(mac_obj.payload)

    return (ip.srcLan, ip.srcHost, ip.destLan, ip.destHost, ip.payload)

class UDP(object):
    def __init__(self, srcPort, destPort=False, payload=False):
        if destPort:
            self.srcPort = srcPort
            self.destPort = destPort
            self.payload = payload
            self.packet = self.srcPort + self.destPort + self.payload
        else:
            self.parse(srcPort)

        if len(self.srcPort) == 1:
            self.srcPort = "0" + self.srcPort

        if len(self.destPort) == 1:
            self.destPort = "0" + self.destPort

        if len(self.srcPort) != 2 or len(self.destPort) != 2:
            raise ValueError

    def parse(self, packet):
        self.packet = packet
        self.srcPort = packet[0:2]
        self.destPort = packet[2:4]
        self.payload = packet[4:]

class IP(object):
    def __init__(self, srcLan, srcHost=False, destLan=False, destHost=False, nextProtocol=False, payload=False):
        if srcHost:
            self.srcLan = srcLan
            self.srcHost = srcHost
            self.destLan = destLan
            self.destHost = destHost
            self.nextProtocol = nextProtocol
            self.cksum = checksum(bytearray(srcLan+srcHost+destLan+destHost+nextProtocol, encoding="UTF-8")).decode("UTF-8")
            self.payload = payload
            self.packet = srcLan + srcHost + destLan + destHost + nextProtocol + self.cksum + payload
        else:
            self.parse(srcLan)

    def parse(self, packet):
        self.packet = packet
        self.srcLan = packet[0:1]
        self.srcHost = packet[1:2]
        self.destLan = packet[2:3]
        self.destHost = packet[3:4]
        self.nextProtocol = packet[4:5]
        self.cksum = packet[5:9]
        self.payload = packet[9:]


if __name__ == "__main__":
    packet = encode_ip(encode_udp(("01", "C", "1", "01", "C", "2", "HELLO")))
    print(packet)
    info = decode_udp(decode_ip(packet))
    print(info)

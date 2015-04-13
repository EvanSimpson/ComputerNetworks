import socket
import json
from UDP import encode_udp, decode_udp, encode_ip, decode_ip

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with sock as s:
        source = ("A3", "3")
        # param_tuple = (srcPort, srcLan, srcHost, destPort, destLan, destHost, payload)
        payload = encode_ip(encode_udp(("03", "A", "3", "02", "C", "1", "HELLO LAN")))[2]
        message = json.dumps([{'payload': payload, 'address': source}])
        s.sendto(bytearray(message, encoding="UTF-8"), ('127.0.0.1', 2048))

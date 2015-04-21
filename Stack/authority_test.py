import sys
import socket

localhost = "127.0.0.1"
hostport = 5002

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.sendto(bytearray('port_plz', encoding="UTF-8"), (localhost, hostport))
    (from_authority, authority_addr) =  sock.recvfrom(1024)
    sock.sendto(bytearray('close', encoding="UTF-8"), (localhost, hostport))

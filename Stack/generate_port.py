import sys
import socket

localhost = "127.0.0.1"
hostport = 5002

class PortAuthority(object):
    def __init__(self):
        self.ports = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def generate_port_num(self, sys_addr):
        ports = self.ports.keys()
        for i in range(100):
            if i not in ports:
                self.ports[i] = sys_addr
                return i
        return 100


    def free_port_num(self, sys_addr):
        for k,v in self.ports.items():
            if sys_addr = v:
                del self.ports[k]
        return

    def listen(self):
        with self.sock as s:
            s.bind((localhost, hostport))
            while True:
                try:
                    (input_from_client, client_address) = s.recvfrom(1024)
                    inp = input_from_client.decode("UTF-8")
                    if inp == "close":
                        self.free_port_num(client_address)
                    else:
                        port = self.generate_port_num(client_address)
                        s.sendto(bytearray(port), client_address)
                except KeyboardInterrupt:
                    s.close()
                    sys.exit()


if __name__ == "__main__":
    authority = PortAuthority()
    authority.listen()

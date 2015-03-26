"""
MSclienttest.py
---------------
morsocket client testing module. The code here
is taken from Alex Morrow's UDP_TX module and 
simply reorganized, with a different import call.

In theory, it should work identically on the morsocket
as it did on the ordinary socket.
"""


# ----- IMPORTS ------ #
import morsocket as CN_Sockets

class UDP_TX(object):
    def __init__(self,Server_Address=("127.0.0.1",5280)):
        # Pull constants from socket library
        socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM

        with socket(AF_INET,SOCK_DGRAM) as sock:  # open the socket    
            while True: 
                str_message = input("Enter message to send to server:\n")
                if not str_message: break  # Break on empty return
                bytes_sent = sock.sendto(str_message.encode("utf-8"), Server_Address)

        print ("UDP_Client ended")

# ----- TESTING CODE ------ #
if __name__ == "__main__":
    UDP_TX()
"""
morsocket.py
------------
A set of classes to implement basic socket functionality
for the CN-Internet.

The morsocketclient is a socket clone for use by applications.
It should operate as normal sockets would, such that the
application cannot distinguish it from sockets, except for
the import command. Additionally, many applications, each
using morsocketclient, should be able to run simultaneously.

Underlying the morsocketclient is a seperate, singleton process
running the morsocketserver on top of the morse stack (layers 1-4).
morsocketclient and morsocketserver manage cross-process communication
via the normal sockets library.

"""


# ----- IMPORTS ------ #
import socketsbase as sb
import json
import queue
import threading
from interfaces import StackLayer

# Move constants to this namespace
AF_INET = sb.AF_INET
SOCK_DGRAM = sb.SOCK_DGRAM
SOCK_STREAM = sb.SOCK_STREAM

# Internal Constants
_MORSOCK_SERVER_ADDR = ('localhost', 5280)  # Default address of the morstack server
_PORT_CAP = 100  # Number of morse ports to make available

class socket(sb.socketbase):
    """
    Serves as a sockets-conforming interface for use by the
    application layer. Implements bind, recvfrom, and sendto
    as expected of a normal socket, but forwards method calls
    to the morse-stack via RPC.
    """

    def __init__(self, network_protocol=AF_INET, transport_protocol=SOCK_DGRAM):
        self.msg_queue = queue.Queue()
        self.CMD_MAP = {
            "exception" : self._raiseException,
            "message" : self._enqueueMessage
        }
        
        super().__init__(network_protocol, transport_protocol) 
        
        self.sock = sb.CN_Socket(2, 2)
        threading.Thread(target=self._internal_recv).start()
        self.sock.sendto(serialize("register"), _MORSOCK_SERVER_ADDR)
        
    def _internal_recv(self):
        while True:
            data, addr = self.sock.recvfrom(8192)
            data = deserialize(data)
            self.CMD_MAP[data["instruction"]](**data["params"])
            
    def _enqueueMessage(self, message, addr):
        self.msg_queue.put((message, addr))
        
    def _raiseException(self, desc):
        raise Exception(desc)
        
    def bind (self, addr):
        serialized = serialize("bind", {
                "request_addr": addr
            })
                
        self.sock.sendto(serialized, _MORSOCK_SERVER_ADDR)
    
    def recvfrom (self, bufsize):
        try:
            return self.msg_queue.get(True, self.timeout)
        except queue.Empty:
            raise TimeoutException("Socket recvfrom operation timed out.")
    
    def sendto (self, message, address):
        serialized = serialize("sendto", {
                "message": forcedecode(message),
                "address": address
            })
                
        self.sock.sendto((serialized), _MORSOCK_SERVER_ADDR)
        
class socketserver (StackLayer):
    
    def __init__ (self, addr=_MORSOCK_SERVER_ADDR, verbose=False):
        self.verbose = verbose
        self.port_map = {}
        self.port_counter = 0
        self.CMD_MAP = {
            "sendto" : self.passDown,
            "bind" : self.bind,
            "register" : self.register
        }
        
        with sb.CN_Socket(2, 2) as self.sock:
            self.sock.bind(addr)          
            while True:
                data, addr = self.sock.recvfrom(8192)
                cmd_obj = deserialize(data)
                cmd_obj['params']['addr'] = addr
                self.CMD_MAP[cmd_obj['instruction']](**cmd_obj['params'])
                if self.verbose: print("Received the command {} from {}".format(data, addr))
                
        self.sock.close()

    def passUp(self, msg):
        """
        Grab IP/Port data and forward through internal socket to the
        related process in the port_map.
        """
        pass
        
    def passDown (self, message, addr):
        """
        Sequence data into a layer 3+4 packet and pass down the stack.
        """
        pass
                
    
    def bind (self, request_addr, addr):
        """
        Binds a process to the requested (ip, port) address if that combination
        is not already in use by another process. Returns a serialized exception
        to the requesting morstackclient if the address is not available
        """
        
        if request_addr in self.port_map.itervalues():
            exception = "Port in use"
        elif request_addr[1] > _PORT_CAP:
            exception = "Port number out of range. Ports numbers must be >0 and <{}".format(_PORT_CAP)
        else:
            self.port_map[addr[1]] = request_addr[1]
            if self.verbose: print("Process on OS port {} bound to morse port {}".format(addr[1], request_addr[1]))
            return
        
        self.sendException(exception, addr)
            
    
    def register (self, addr):
        """
        Assign a morse port to a process when it starts up. The ports
        are assigned from 0 to _PORT_CAP and will find an available port
        if available. If a port is not available, it will return a serialized
        exception to the morstackclient.
        """
        
        for i in range(self.port_counter, self.port_counter + _PORT_CAP):
            port = i % _PORT_CAP
            
            # If an available port if found, adjust the port_counter for
            # future searches, and register the process to the port
            if port not in self.port_map:
                self.port_counter = port + 1
                self.port_map[addr[1]] = port
                if self.verbose: print("New process registered on OS port {} bound to morse port {}".format(addr[1], port))
                return
        
        # If no ports are available, forward an exception to the requesting client
        self.sendException("No ports available", addr)
        
    def sendException(self, desc, addr):
        self.sock.sendto(serialize("exception", {"desc": desc}), addr)
        
def serialize (instruction, parameters={}):
    return json.dumps(
        {"instruction": instruction,
         "params": parameters
        }).encode('utf-8')
    
def deserialize (serialized):
    return json.loads(serialized.decode('utf-8'))
    
def forcedecode (encoded):
    try:
        return encoded.decode('utf-8')
    except TypeError:
        return encoded
    
    
# ----- TESTING CODE ----- #
if __name__ == "__main__":
    print("-- Testing: ")
    with socket(AF_INET, SOCK_DGRAM) as test_sock:
        pass
        
        
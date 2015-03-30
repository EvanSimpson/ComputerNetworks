import json
import socket
import generate_port

localhost = '127.0.0.1'
stack_port = 5000
olinhost = 'A'

class JoeSocket(object):
    def __init__(self, family=socket.AF_INET, n_type=socket.SOCK_STREAM, proto=0):
        self._family = family
        self._type = n_type
        self._proto = proto
        self._closed = False
        self._stack_address = (localhost, stack_port)
        self._pysock = False
        self._address = ()
        # TODO get port from port authority at some point

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self._closed:
            self.close()

    def _initialize_socket(self):
        self._pysock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._address = (olinhost, "01")

    def bind(self, address):
        # Bind the socket to address. The socket must not already be bound.
        # (The format of address depends on the address family — see above.)
        if not self._pysock:
            self._initialize_socket()
        try:
            payload = bytearray(json.dumps({'command': 'bind', 'params': {'source_address': self._address}}))
            sent = self._pysock.sendto(payload)
            while 1:
                try:
                    from_stack, stack_address = self._pysock.recvfrom(1024)
                    response = json.loads(from_stack.decode("UTF-8"))
                    if response.error != 0:
                        # TODO error handling here
                        pass
                    else:
                        return 0
                except:
                    # TODO check error to make sure socket is still open
                    continue
        except:
            # TODO error handling here
            pass

    def close(self):
        # Mark the socket closed. The underlying system resource (e.g. a file
        # descriptor) is also closed when all file objects from makefile() are
        # closed. Once that happens, all future operations on the socket object
        # will fail. The remote end will receive no more data (after queued data
        # is flushed).
        #
        # Sockets are automatically closed when they are garbage-collected, but
        # it is recommended to close() them explicitly, or to use a with
        # statement around them.
        #
        # Note close() releases the resource associated with a connection but
        # does not necessarily close the connection immediately. If you want
        # to close the connection in a timely fashion, call shutdown() before
        # close().
        if not self._pysock:
            # TODO Error - no socket to close
            pass
        try:
            payload = bytearray(json.dumps({"command":"close", "params": {"source_address": {self._address}}}))
            sent = self._pysock.sendto(payload)
            while 1:
                from_stack, stack_address = self._pysock.recvfrom(1024)
                response = json.loads(from_stack.decode("UTF-8"))
                if response.error != 0:
                    # TODO error handling here
                    pass
                else:
                    return 0
        except:
            # TODO check error to make sure socket is still open
            pass
        self._closed = True
        self._pysock.close()

    def recvfrom(self, buffsize, flags):
        # Receive data from the socket. The return value is a pair
        # (bytes, address) where bytes is a bytes object representing the data
        # received and address is the address of the socket sending the data.
        # See the Unix manual page recv(2) for the meaning of the optional
        # argument flags; it defaults to zero. (The format of address depends
        # on the address family — see above.)
        if not self._pysock:
            self._initialize_socket()
        try:
            #TODO this length needs to take into account the additional
            #     bytes for string formatting extra socket info
            from_stack, stack_address = self._pysock.recvfrom(1024, self._stack_address)
            response = json.loads(from_stack.decode("UTF-8"))
            return (response.payload, response.address)
        except:
            #TODO throw the same error that the pysocket would have thrown
            pass

    def sendto(self, send_bytes, address):
        # Send data to the socket. The socket should not be connected to a
        # remote socket, since the destination socket is specified by address.
        # The optional flags argument has the same meaning as for recv() above.
        # Return the number of bytes sent. (The format of address depends on the
        # address family — see above.)
        if not self._pysock:
            self._initialize_socket()
        if len(send_bytes):
            payload = bytearray(json.dumps({"command":"sendto", "params": {"source_address": self._address, "destination_address": address, "data": send_bytes.decode("utf-8")}}), encoding="utf-8")
            sent = self._pysock.sendto(payload, self._stack_address)
        else:
            #error
            pass

if __name__ == "__main__":
    sock = JoeSocket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytearray("HI TEAM LETS TEST YAY BABYSTEPS", encoding="utf-8"), ("A", "01"))

import json
import socket

localhost = '127.0.0.1'
stack_port = 5000

class JoeSocket(Object):
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0):
        self._family = family
        self._type = type
        self._proto = proto
        self._stack_address = (localhost, stack_port)
        # TODO initialize socket to stack somewhere
        # TODO get port from port authority at some point

    def bind(self, address):
        # Bind the socket to address. The socket must not already be bound.
        # (The format of address depends on the address family — see above.)
        if not self._pysock:
            # TODO open a new socket to the Stack
        try:
            payload = bytearray(json.dumps({'command': 'bind', 'params': {'address': self._address}}))
            sent = self._pysock.sendto(payload)
            while 1:
                try:
                    from_stack, stack_address = self._pysock.recvfrom(1024)
                    response = json.loads(from_stack.decode("UTF-8"))
                    if response.error != 0:
                        # TODO error handling here
                    else
                        return 0
                except:
                    # TODO check error to make sure socket is still open
                    continue
        except:
            # TODO error handling here

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
        try:
            payload = bytearray(json.dumps({"command":"close", "params": {"address": {self._address}}}))
            sent = self._pysock.sendto(payload)
            while 1:
                from_stack, stack_address = self._pysock.recvfrom(1024)
                response = json.loads(from_stack.decode("UTF-8"))
                if response.error != 0:
                    # TODO error handling here
                else
                    return 0
            except:
                # TODO check error to make sure socket is still open
                continue
        except:
            # TODO check error to make sure socket is still open

    def recvfrom(self, buffsize, flags):
        # Receive data from the socket. The return value is a pair
        # (bytes, address) where bytes is a bytes object representing the data
        # received and address is the address of the socket sending the data.
        # See the Unix manual page recv(2) for the meaning of the optional
        # argument flags; it defaults to zero. (The format of address depends
        # on the address family — see above.)
        if not self._pysock:
            # TODO open the socket to Stack
        try:
            #TODO this length needs to take into account the additional
            #     bytes for string formatting extra socket info
            from_stack, stack_address = self._pysock.recv(1024)
            response = from_stack.decode("UTF-8")
            if response.error != 0:
                #TODO verify the from_stack data here
            else:
                return response.data
        except:
            #TODO throw the same error that the pysocket would have thrown

    def sendto(self, bytes, address):
        # Send data to the socket. The socket should not be connected to a
        # remote socket, since the destination socket is specified by address.
        # The optional flags argument has the same meaning as for recv() above.
        # Return the number of bytes sent. (The format of address depends on the
        # address family — see above.)
        if not self._pysock:
            # ERROR
        else:
            sent = 0
            if len(string):
                #TODO serialize string and JoeSocket info before sending
                sent = self._pysock.sendto(string, self._stack_address)
            if sent==len(string):
                while 1:
                    try:
                        from_stack, stack_address = self._pysock.recvfrom(1024)
                        return sent
                    except:
                        continue
            else:
                #error

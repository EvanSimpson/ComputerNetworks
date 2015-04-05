import sys
import sockets
import pi
import threading

localhost = '127.0.0.1'
ownport = 5003

# Have to use an object as a flag so the value is passed as reference
class RecvFlag():
    def __init__(self):
        self.flag = False

recv_flag = RecvFlag()
recv_flag_lock = threading.Lock()

send_buffer = []
send_buffer_lock = threading.Lock()


def recv_run():
    for data in pi.receive(recv_flag_lock, recv_flag):
        send_buffer_lock.acquire()
        send_buffer.append(data)
        send_buffer_lock.release()


class GPIOServe(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INTET, socket.SOCK_DGRAM)
        self.stack_address = False

        self.recv_thread = threading.Thread(target=recv_run)



    def listen(self):
        with self.sock as s:
            s.bind((localhost, ownport))

            # Start the GPIO receive thread
            recv_flag.flag = True
            self.recv_thread.run()

            while True:
                try:

                    # Check if something has come in from the GPIO and send it
                    # over to the stack if so
                    send_buffer_lock.acquire()
                    if len(send_buffer) > 0 and self.stack_address:
                        s.sendto(bytearray(send_buffer[0], encoding="UTF-8"), self.stack_address)
                        del send_buffer[0]
                    send_buffer_lock.release()

                    # Check if something has come in from the stack and send it
                    # over to the GPIO if so
                    (from_stack, stack_address) = s.recvfrom(1024)
                    self.stack_address = stack_address
                    data = from_stack.decode("UTF-8")
                    if len(data) > 1:
                        pi.transmit(data)


                except KeyboardInterrupt:
                    # Shut it down
                    recv_flag_lock.acquire()
                    recv_flag.flag = False
                    recv_flag_lock.release()
                    s.close()
                    pi.kill()
                    sys.exit()

if __name__ == "__main__":

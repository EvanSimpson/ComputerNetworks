import sys
import socket
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
        if send_buffer_lock.acquire():
            send_buffer.append(data)
            send_buffer_lock.release()


class GPIOServe(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.stack_address = False

        self.recv_thread = threading.Thread(target=recv_run)



    def listen(self):
        with self.sock as s:
            s.bind((localhost, ownport))
            s.setblocking(False)

            # Start the GPIO receive thread
            recv_flag.flag = True
            self.recv_thread.start()

            while True:
                try:
                    # Check if something has come in from the GPIO and send it
                    # over to the stack if so
                    if send_buffer_lock.acquire():
                        if len(send_buffer) > 0 and self.stack_address:
                            print("got a message to send to stack" + str(send_buffer))
                            s.sendto(bytearray(send_buffer[0], encoding="UTF-8"), self.stack_address)
                            del send_buffer[0]
                        send_buffer_lock.release()

                except KeyboardInterrupt:
                    # Shut it down
                    if recv_flag_lock.acquire():
                         recv_flag.flag = False
                         recv_flag_lock.release()
                    s.close()
                    pi.kill()
                    sys.exit()


                try:
                    # Check if something has come in from the stack and send it
                    # over to the GPIO if so
                    (from_stack, stack_address) = s.recvfrom(1024)
                    self.stack_address = stack_address
                    print("Received data from stack")
                    data = from_stack.decode("UTF-8")
                    print(data)
                    if len(data) > 1:
                        print("about to transmit over the pi")
                        pi.transmit(data)

                except socket.error:
                    continue

                except KeyboardInterrupt:
                    # Shut it down
                    if recv_flag_lock.acquire():
                        recv_flag.flag = False
                        recv_flag_lock.release()
                    s.close()
                    pi.kill()
                    sys.exit()


if __name__ == "__main__":
    server = GPIOServe()
    server.listen()

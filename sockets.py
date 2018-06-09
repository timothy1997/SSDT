# Link to reference: https://docs.python.org/3/howto/sockets.html

import sys
import socket
import SocketsHeader

class MySocket:
    # For demonstration only, not a great implementation
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

def Main():
    # Ask what the user wants to do...
    response = int(input("0.) Quit\n1.) Host a conversation\n2.) Connect to conversation\n"))

    if response == 1:
        socket1 = MySocket()
        # Create an INET (IPv4), STREAMing (TCP) socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serversocket.bind((socket.gethostname(), 65534))
        # "become" a socket
        serversocket.listen(5)
        # accept a connection from outside
        (clientsocket, address) = serversocket.accept()
        serversocket.close()
        print(clientsocket)
        print(address)
    elif response == 2:
        hostname = input("Hostname: ")
        socket2 = MySocket()
        socket2.connect(hostname, 65534)
        socket2.close()
    else:
        return

if __name__ == "__main__":
    Main()

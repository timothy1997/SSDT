# Link to reference: https://docs.python.org/3/howto/sockets.html

import sys
import socket
import math

encoding = 'utf-8'

def Main():
    # Ask what the user wants to do...
    response = int(input("0.) Quit\n1.) Host a conversation\n2.) Connect to conversation\n"))

    if response == 1:
        # Create an INET (IPv4), STREAMing (TCP) socket.
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        # if we binded to 'localhost' or '127.0.0.1', we would still have
        # a server socket, but only visible within the same machine
        # s.bind('', 80) specifies that the socket is reachable by any
        # address the machine happens to have
        serversocket.bind((socket.gethostname(), 8080))
        # "become" a socket, that is listening for 5 connections
        serversocket.listen(5)
        # accept a connection from outside
        (clientsocket, address) = serversocket.accept()
        # get the size of the message, and compute how many chunks that will be
        message = clientsocket.recv(32)
        message = message.decode(encoding)
        chunks = math.ceil(int(message) / 8192)
        # send to the client that the message was received, and that they may begin sending
        clientsocket.send('1'.encode(encoding))
        clientsocket.close()
    elif response == 2:
        hostname = input("Hostname: ")
        message = input("Message Size: ")
        # Create a client socket
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the serversocket
        clientsocket.connect((hostname, 8080))
        # Send them the data
        clientsocket.send(message.encode(encoding))
        verification = clientsocket.recv(1)
        str(verification.decode(encoding))
        print(verification)
        if verification == '1':
            print("Verification received, beginning message transmition sequence...")
        else:
            print("Some error occured...")
        clientsocket.close()
    else:
        return

if __name__ == "__main__":
    Main()

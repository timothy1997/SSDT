# Link to reference: https://docs.python.org/3/howto/sockets.html

import sys
import socket
import math

# global values
encoding = 'utf-8'
chunksize = 8

def Main():
    # Ask what the user wants to do...
    response = int(input('0.) Quit\n1.) Host a conversation\n2.) Connect to conversation\n'))

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
        # get the size of the message, decode it, and compute how many chunks that will be
        message = clientsocket.recv(32)
        message = message.decode(encoding)
        chunksnum = math.ceil(int(message) / chunksize)
        # send to the client that the message was received, and that they may begin sending
        clientsocket.send('1'.encode(encoding))
        # begin receiving the message
        # The total number of chunks
        currentchunk = 0
        chunks = []
        while currentchunk < chunksnum:
            chunk = clientsocket.recv(chunksize)
            chunks.append(chunk)
            currentchunk += 1
        i = 0
        while i < len(chunks):
            chunks[i] = chunks[i].decode(encoding)
            i += 1
        clientsocket.close()
        finalMessage = "".join(chunks)
        print(finalMessage)
    elif response == 2:
        # hostname = input('Hostname: ')
        # message = input('Message: ')
        hostname = 'tim-Inspiron-7352'
        message = 'This is a message to all the people on earth. My name is Tim Sherry.'
        messagesize = len(message)
        # Create a client socket
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the serversocket
        clientsocket.connect((hostname, 8080))
        # Send them the data
        clientsocket.send(str(messagesize).encode(encoding))
        # Receive the verification
        verification = clientsocket.recv(1)
        verification = verification.decode(encoding)
        # If the verification message is one, begin transmitting the message. Otherwise, don't.
        if verification == '1':
            # The total number of chunks
            chunksnum = math.ceil(float(messagesize) / chunksize)
            currentchunk = 0
            while currentchunk < chunksnum:
                if currentchunk < (chunksnum - 1):
                    tosend = message[currentchunk*chunksize:(currentchunk*chunksize)+chunksize]
                    sent = clientsocket.send(tosend.encode(encoding))
                else:
                    tosend = message[currentchunk*chunksize:]
                    sent = clientsocket.send(tosend.encode(encoding))
                currentchunk += 1
                if sent == 0:
                    raise RuntimeError("socket connection broken")
        else:
            print("Some error occured...")
        clientsocket.close()
    else:
        return

if __name__ == "__main__":
    Main()

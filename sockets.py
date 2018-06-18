# Link to reference: https://docs.python.org/3/howto/sockets.html

import sys
import socket
import math
import os, os.path

# global values
encoding = 'utf-8'
chunksize = 4096

def Main():
    # Ask what the user wants to do...
    response = int(input('0.) Quit\n1.) Host a conversation\n2.) Connect to conversation\n'))

    if response == 1: # (Host)
        # What's happening here:
        # Create an INET (IPv4), STREAMing (TCP) socket, and bind the socket to a public host, and a
        # well-known port. If we binded to 'localhost' or '127.0.0.1', we would still have a server
        # socket, but only visible within the same machine. s.bind('', 80) specifies that the socket
        # is reachable by any address the machine happens to have. The socket will listen for 5
        # connections (eventually I want to implement this part using threads), and accept one. At
        # this point, it will receive the size of the message by the user, and compute how many chunks
        # that will be. It will then send a verification to the client, and the client will start sending
        # the message. We first receive the name of the file, then we receive the chunks, decode them,
        # save them in an array, then join them, outputing the message.
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((socket.gethostname(), 8080))
        serversocket.listen(5)
        (clientsocket, address) = serversocket.accept()
        os.makedirs(address[0])
        print("Connection made...\n")

        filenum = clientsocket.recv(32).decode(encoding)
        clientsocket.send('1'.encode(encoding))

        for i in range(0, int(filenum)):
            message = clientsocket.recv(32).decode(encoding)
            chunksnum = math.ceil(int(message) / chunksize)
            clientsocket.send('1'.encode(encoding))
            filename = ''
            chunks = []
            currentchunk = 0
            filename = clientsocket.recv(chunksize).decode()
            while currentchunk < chunksnum:
                chunk = clientsocket.recv(chunksize).decode(encoding)
                chunks.append(chunk)
                currentchunk += 1
            finalMessage = "".join(chunks)
            f = open(address[0] + '/' + filename, 'w+')
        clientsocket.close()
    elif response == 2: # (Client)
        # What's going on here: We get the hostname and the file to be sent, then we read the contents
        # of the file. We create a socket that utilizes an IPv4, TCP connection, and send them the size
        # of the file (which is info that they will need). We receive a verification message, we indicates
        # whether they received the message or not. If they did, we send them the entire message
        # hostname = input('Hostname: ')
        # directory = input('Directory: ')
        hostname = 'tim-Inspiron-7352'
        directory = '/home/tim/Desktop/SSDT/Speeches'

        # connect with the host
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((hostname, 8080))

        # send the host the number of files we're dealing with
        filenum = 0
        for nfile in os.listdir(directory):
            if not os.path.isfile(nfile):
                filenum += 1
        clientsocket.send(str(filenum).encode(encoding))

        # If they send back '1'
        fverification = clientsocket.recv(1)
        fverification = fverification.decode(encoding)
        if fverification == '1':
            # Send them all the files isn the directory
            for nfile in os.listdir(directory):
                filename = os.path.basename(nfile)
                if not os.path.isfile(directory + '/' + nfile):
                    continue
                with open(directory + '/' + nfile) as b:
                    message = b.read()
                clientsocket.send(str(len(message)).encode(encoding))
                verification = clientsocket.recv(1)
                verification = verification.decode(encoding)
                if verification == '1':
                    # What's going on here: We calculate the number of chunks we will send, and send the name
                    # of the file. Then we begin sending the actual message. While there are still chunks to
                    # send (currentchunk keeps track) of the chunks sent), we must send them. If the current
                    # chunk to be sent is not the last one, you send 4096 bytes. Otherwise, we just send the
                    # rest of the bytes. If 0 is returned, then something went wrong.
                    chunksnum = math.ceil(float(len(message)) / chunksize)
                    currentchunk = 0
                    clientsocket.send(filename.encode(encoding))
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

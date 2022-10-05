from email import message
from http import client
import socket

#Se especifíca el protocolo SOCK_STREAM = TCP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

host = socket.gethostbyname("localhost")
port = 444

serversocket.bind((host,port))

serversocket.listen(25)

while True:
    clientsocket, address = serversocket.accept()

    print("Received connection from {}".format(str(address)))

    msg = "Thank you for connecting to the server\n"

    clientsocket.send(msg)

    clientsocket.close()

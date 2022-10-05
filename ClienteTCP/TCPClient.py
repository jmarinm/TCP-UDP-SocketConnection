from email import message
import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 444

clientsocket.connect(('192.168.60.128'.port))

msg = clientsocket.recv(1024)

clientsocket.close()

print(msg.decode('ascii'))
import socket
import threading


 

host = '0.0.0.0'
port = 444


def main():
    #Se especifíca el protocolo SOCK_STREAM = TCP
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host,port))
    serversocket.listen(25)
    print(f'[*] Listening on {host}:{port}')

    while True:
        client, address = serversocket.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == "__main__":
    main()

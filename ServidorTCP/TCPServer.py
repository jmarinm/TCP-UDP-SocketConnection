import hashlib
import socket
import threading
import pickle
import time


 

host = '0.0.0.0'
port = 448


serverMessages = {
    "filesCatalog": b"Which size of file do you want to transfer?\n1 - 250mb file. \n2 - 100mb file\n"
}

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
        
        clientId = sock.recv(1024).decode()
        sock.send(serverMessages['filesCatalog'])
        request = sock.recv(1024).decode("utf-8")
        print(f'[*] Received: {request} from Client {clientId}')
        if request[0] == "1":
            file = open('ServidorTCP/Files/250.img','rb') #sock.send(b'250 file')
        elif request[0] == "2":
            file = open('ServidorTCP/Files/100.img','rb')#sock.send(b'100 file')
        
        file = file.read()
        hash = hashlib.md5(file).hexdigest()
        fileData = [file, hash]
        print(f'[*] Hash: {hash} - Client: {clientId}')
        t_inicial = time.time()
        sock.send(pickle.dumps(fileData))
        t_final = time.time()
        print(f'[*] Transfer Time {t_final-t_inicial}')

        sock.close()
        
if __name__ == "__main__":
    main()

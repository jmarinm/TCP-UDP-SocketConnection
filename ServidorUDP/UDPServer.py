from fileinput import filename
import hashlib
import socket
import threading
import pickle
import sys
import time
import os

 

host = '0.0.0.0'
port = 449
TAM_MSG = 1024 


serverMessages = {
    "filesCatalog": b"Which size of file do you want to transfer?\n1 - 250mb file. \n2 - 100mb file\n"
}

def main():
    #Se especifíca el protocolo SOCK_DGRAM = UDP
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind((host,port))
    print(f'[*] Listening on {host}:{port}')

    while True:
        data, address = serversocket.recvfrom(1024)
        print(f'[*] Message Received From {address[0]}:{address[1]}, Content: {data.decode("utf-8")}')
        client_handler = threading.Thread(target=handle_message,args=(data,address, serversocket))
        client_handler.start()

def handle_message(msg, addr, serversocket):
    
    msg = msg.decode("utf-8")
    clientId, fileno = msg.split("-")
    print(f"[*] Received request from Client {clientId}")

    if fileno == "1": filename = "250.txt"
    else: filename = "100.txt"

    print(f"[*] Starting to send file '{filename}' to Client {clientId}")

    file = open(f'ServidorUDP/ServerFiles/{filename}','rb')
    t_inicial = time.time()
    send_file(file,serversocket, addr)
    t_final = time.time()
    t_time = t_final-t_inicial
    bytesTransfered = os.path.getsize("ServidorUDP/ServerFiles/"+filename)
    print(f"[*] Envío de archivo finalizado para el Cliente {clientId}")
    print(f'[*] Transfer Time {round(t_time,2)}s for client {clientId}')
    print(f'[*] Transfer Rate for Client {clientId}: {round((bytesTransfered/(2**20))/t_time,2)}MB/s')
    print(f'[*] Bytes transfered {bytesTransfered} for client {clientId}')


def send_file(file,socket, addr):

    portion = file.read(TAM_MSG)
    while portion:
        socket.sendto(pickle.dumps(portion),addr)
        portion = file.read(TAM_MSG)
    

    
if __name__ == "__main__":
    main()

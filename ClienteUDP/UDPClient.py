from datetime import datetime
import os
import threading
import socket
import pickle
import hashlib
import time

target_host = "192.168.60.128"
target_port = 449
bufSize = 300*(8**6)
addr = (target_host,target_port)



def client(client,id,fileid,logfile):
    with open(logfile+'-'+str(id)+'.txt', 'w') as log:
        option = fileid
        if option == "1": filename = f"250-{id}.txt"
        elif option == "2":filename = f"100-{id}.txt"

        log.write(f"[*] Filename: {filename}\n")

        #Formato de la petición es <idCliente>-<nombreArchivo>
        clientRequest = f"{id}-{option}"

        #Communication
        client.sendto(clientRequest.encode("utf-8"),addr)

        data = b""
        try:
            while True:
                #Timeout para saber cuando ya se dejó de transmitir el archivo.
                client.settimeout(5)
                packet, dire = client.recvfrom(4096)
                data+= packet
        except Exception as e:
            print(e)
            print("[*] Transmisión Finalizada")

        with open('ClienteUDP/ArchivosRecibidos/'+filename, 'wb') as f:
            f.write(data)
            log.write(f"[*] : File was saved for client {id}\n") 
            f.close()
        
        if option == "1": filesize = 262144000
        elif option == "2":filesize = 104857600

        size = os.path.getsize("ClienteUDP/ArchivosRecibidos/"+filename)
        print(f"[*] Size of received file '{filename}' is {round(size/(2**20),2)} MBs")
        if size == filesize:
            log.write(f"[*] : Transfer Was Succesful for client {id}\n")
            print(f"[*] : Transfer Was Succesful for client {id}\n")
        else:
            log.write(f"[*] : Transfer Was Not Succesful for client {id}\n")
            print(f"[*] : Transfer Was Not Succesful for client {id}\n")

        

def main():
    n = input("Que número de clientes desea conectar: ")
    file = input("Ingrese 1 si desea descargar el archivo de 250 mb , o 2 si desea el de 100 mb ")
    logname = 'ClienteUDP/Logs/'+str(datetime.now()).replace(" ", "").replace(".","",1).replace(":","-")
    for i in range(int(n)):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_handler = threading.Thread(target=client, args=(client_socket,i+1,file, logname))
        client_handler.start()

if __name__ == "__main__":
    main()
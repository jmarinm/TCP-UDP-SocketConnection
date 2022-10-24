from datetime import datetime
import threading
import socket
import pickle
import hashlib
import time

target_host = "localhost"#"192.168.60.128"
target_port = 449
bufSize = 300*(8**6)




def client(client,id,fileid,logfile):
    with open(logfile+'-'+str(id)+'.txt', 'w') as log:
        option = fileid
        if option == "1": filename = "250.img"
        elif option == "2":filename = "100.img"

        log.write(f"[*] Filename: {filename}\n")

        client.connect((target_host,target_port))


        #Communication
        client.send(str(id).encode())
        filesMenu = client.recv(1024)
        
        client.send(option.encode())

        data = []
        while True:
            packet = client.recv(4096)
            if not packet: break
            data.append(packet)
        data_arr = pickle.loads(b"".join(data))

        if len(data_arr) >= 2 and data_arr[0]:
            log.write(f"[*] : Transfer Was Succesful for client {id}\n")
        else:
            log.write(f"[*] : Transfer Was Not Succesful for client {id}\n") 

        calculated_hash = hashlib.md5(data_arr[0]).hexdigest()
        if calculated_hash== data_arr[1]:
            log.write(f"[*] : Hash is correct for client {id}\n") 
            print(f"Client {id} - Hash Is Correct for client {id}")
        else:
            log.write(f"[*] : Hash is incorrect for client {id}\n") 
            print(f"Client {id} - Hash Is Incorrect for client {id}")
        

        with open('ClienteTCP/ArchivosRecibidos/'+filename+"-"+str(id), 'wb') as f:
            f.write(data_arr[0])
            log.write(f"[*] : File was saved for client {id}\n") 
            f.close()
        
        time = client.recv(4096*2)
        print(f'Client {id} - Transfer Time: {time}')
        log.write(f"[*] : Transfer time: {time} for client {id}\n") 


        client.close()

def main():
    n = input("Que número de clientes desea conectar: ")
    file = input("Ingrese 1 si desea descargar el archivo de 250 mb , o 2 si desea el de 100 mb ")
    logname = 'ClienteTCP/Logs/'+str(datetime.now()).replace(" ", "").replace(".","",1).replace(":","-")
    for i in range(int(n)):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_handler = threading.Thread(target=client, args=(client_socket,i+1,file, logname))
        client_handler.start()

if __name__ == "__main__":
    main()
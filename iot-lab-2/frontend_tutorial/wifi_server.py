import socket
import os
from dotenv import load_dotenv
from _thread import *
import threading

load_dotenv()

HOST = os.getenv('IP_ADDRESS') # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

lock = threading.Lock()

def threaded(client,clientInfo):
    while 1:
        data = client.recv(1024)
        if not data:
            break
        data = data.decode()
        print(data)

    #close client socket
    print('closing connection to:',clientInfo[0])

    #release lock
    lock.release()

    #close client socket
    client.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    try:
        while 1:
            #accept new client connections
            client, clientInfo = s.accept()
            #lock acquired by a client
            lock.acquire()
            print("Connected to: ", clientInfo[0])
            #start a new thread for client
            start_new_thread(threaded, (client,clientInfo))
    except:
        print("Closing server socket")
        s.close()
 

        
            

if __name__ == '__main__':
    main()
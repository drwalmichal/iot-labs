import socket
import os
from dotenv import load_dotenv
import picar_4wd as fc
load_dotenv()

HOST = os.getenv('IP_ADDRESS') # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)


power_val = 10

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    try:
        while 1:
            #accept new client connections
            client, clientInfo = s.accept()
            data = client.recv(1024)
            if data == b'up\r\n':
                fc.forward(power_val)
            elif data == b'down\r\n':
                fc.backward(power_val)
            elif data == b'right\r\n':
                fc.turn_right(power_val)
            elif data == b'left\r\n':
                fc.turn_left(power_val)
            elif data == b'stop\r\n':
                fc.stop()
            elif data == b'update\r\n':
                info = f'{fc.get_distance_at(-2)},{fc.power_read()},{fc.utils.cpu_temperature()}'
                client.sendall(info.encode())
            client.close()
    except:
        # print("Closing server socket")
        s.close()
 

if __name__ == '__main__':
    main()
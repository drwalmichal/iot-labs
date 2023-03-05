import socket
import os
from dotenv import load_dotenv
import sys
import tty
import termios
import asyncio

#code from keyboard_control.py in picar-4wd examples
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
    return ch
def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

load_dotenv()

HOST = os.getenv('IP_ADDRESS') # IP address of your Raspberry PI
PORT = 65432          # The port used by the server

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        while 1:
            key = readkey()
            s.send(key.encode())     # send the encoded message (send in binary format)
            if key == 'q':
                raise KeyboardInterrupt
    except:
        print('closing socket')
        s.close()

if __name__ == '__main__':
    main()

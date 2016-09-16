__author__ = 'Abhi'
import socket
class mySocket:
    def __init__(self,sock=None):
        if sock == None:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        else:
            self.sock = sock
    def connect(self,hpTuple):
        self.sock.connect(hpTuple)
    def sendall(self,msg):
        length = len(msg)
        self.sock.sendall(str(length))
        self.sock.recv(1)
        self.sock.sendall(msg)
    def recv(self,max):
        length = self.sock.recv(max)
        self.sock.sendall('k')
        return self.sock.recv(int(length))

def input1():
    yield 'addforum/1/good/xyz'
    yield 'showforums/1/xyx'
    yield 'exit'


def main():
    MAXSIZE = 1024
    c = mySocket()
    c.connect(('localhost',9998))
    msg = 'Welcome !! Enter Command'
    #inp = input1()
    print msg
    while msg != 'exit':
        msg = raw_input('A:>')
        if len(msg)!=0:
            print 'Sending message:',msg
            c.sendall(msg)
            recvbuff = c.recv(MAXSIZE)
            print recvbuff
    c.sock.close()

if __name__ == '__main__':
    main()

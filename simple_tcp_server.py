import socket
import time

HOST = '127.0.0.1'
PORT = 9888
BUFSIZE = 1024
ADDR = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)

sock.listen(5)

while True:
    print "Waiting for connection"
    client_handler, client_addr = sock.accept()
    print "Connection from ", client_addr
    while True:
        try:
            data = client_handler.recv(BUFSIZE)
        except Exception as e:
            print (e)
            break
        if not data:
            break
    
        s = 'Hi, you said:{} at {}'.format(data, time.ctime())
        client_handler.send(s)
    client_handler.close()
sock.close()

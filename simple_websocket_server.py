import socket
import time
import hashlib
import base64


HOST = '127.0.0.1'
PORT = 9002
BUFSIZE = 1024
ADDR = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(5)

#respone =  "HTTP/1.1 101 Switching Protocols\r\n"
respone = "HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n"
respone += "Upgrade: WebSocket\r\n"
respone += "Connection: Upgrade\r\n"
respone += "Sec-WebSocket-Accept: %s\r\n"

respone = '\
HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\r\n'

def get_sec_key(data):
    lst = data.split("\r\n")
    d = {}
    for line in lst:
        lst  = line.split(":")
        k = lst[0]
        v = lst[1:]
        d[k] = ''.join(v)
    return d 



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
        if len(data) == 0:
            continue
        print 'recv from client>>', data
        param = get_sec_key(data)
        client_sec = param.get("Sec-WebSocket-Key").strip()
        print '>>>%s<<<' % client_sec
        client_sec += '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        has = hashlib.sha1(client_sec)
        ss = has.digest()
        p = base64.b64encode(ss)
        respone = respone % p
        print 'resquest', param
        print '=' * 90
        print 'respone', respone
        #s = 'Hi, you said:{} at {}'.format(data, time.ctime())
        client_handler.send(respone)
    client_handler.close()
sock.close()

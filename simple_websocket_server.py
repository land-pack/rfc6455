import socket
import time
import hashlib
import base64


HOST = '127.0.0.1'
PORT = 9888
BUFSIZE = 1024
ADDR = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(5)

respone =  "HTTP/1.1 101 Switching Protocols\r\n"
respone += "Upgrade: websocket\r\n"
respone += "Connection: upgrade\r\n"
respone += "Sec-WebSocket-Accept: %s\r\n"

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
        if not data:
            break
        param = get_sec_key(data)
        client_sec = param.get("Sec-WebSocket-Key")
        has = hashlib.sha1(client_sec)
        ss = has.digest()
        p = base64.b64encode(ss)
        respone = respone % p
        print 'respone', respone
        #s = 'Hi, you said:{} at {}'.format(data, time.ctime())
        client_handler.send(respone)
    client_handler.close()
sock.close()

import socket
import time

HOST = '127.0.0.1'
PORT = 9886
BUFSIZE = 1024
ADDR = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(5)

respone =  "HTTP/1.1 200 OK\r\n"
respone += "Connection: close\r\n"
respone += "Content-Type: text/html; charset=utf-8\r\n"
respone += "Content-Length:%s\r\n\r\n"
#respone += "Connection: close\r\n\r\n"
content= """<html><body>
            <br /><font color="green" size="7">register successs!
            </p></body></html>"""
content_length = len(content)
respone += content 
respone = respone % content_length 


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
    
        #s = 'Hi, you said:{} at {}'.format(data, time.ctime())
        client_handler.send(respone)
    client_handler.close()
sock.close()

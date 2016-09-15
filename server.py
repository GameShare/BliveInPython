#coding=utf-8
import SocketServer  
import threading
from SocketServer import StreamRequestHandler as SRH  

import time,sched,os

host = '127.0.0.1'  
port = 8883
addr = (host,port) 

class Servers(SRH):  
    def handle(self):  
        print 'got connection from ',self.client_address  
        # self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))  
        while True:  
            data = self.request.recv(1024)  
            if not data:   
                break  
            print data  
            print "RECV from ", self.client_address[0]  
            self.request.send(str(i))


server = SocketServer.ThreadingTCPServer(addr,Servers) 


server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print "Server loop running in thread:", server_thread.name
i = 1
while 1:
	i += 1
	time.sleep(1)






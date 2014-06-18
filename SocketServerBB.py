import socket
import SocketServer
import subprocess
import string
import time

from mergeBB import *

'''#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind(('127.0.0.1', 12345))
   
#become a server socket
serversocket.listen(5)   

while 1:
    c, addr = serversocket.accept()     # Establish connection with client.
    print 'Got connection from', addr
    c.send('Thank you for connecting')
    c.close()                # Close the connection '''
    
    

class MyTcpServer(SocketServer.BaseRequestHandler):
    def recvfile(self, filename):
        print "starting reve input file!"
        self.request.send('ready')
        f = open('server_file/'+filename, 'wb')
        while True:
            data = self.request.recv(4096)
            if data == 'EOF':
                print "recv input file success!"
                break
            f.write(data)
        f.close()
                                        
    def sendfile(self, filename):
        print "starting send output file!"
        time.sleep(1)
        f = open('img/'+filename, 'rb')
        while True:
            data = f.read(4096)
            if not data:
                break
            self.request.send(data)
        f.close()
        time.sleep(1)
        self.request.send('EOF')
        print "send output file success!"
                                    
    def handle(self):
        print "get connection from :",self.client_address
        while True:
            try:
                inputname = self.request.recv(4096)
                print "get file:", inputname  
                if not inputname:
                    print "failed: break the connection!"
                    break               
                else:
                    self.recvfile(inputname)
                    
                    iname = mergeBB('server_file/'+inputname)
                    
                    outputname = 'aggBB_info.csv'
                    self.request.send(outputname)
                    self.sendfile(outputname)
                    outputname = 'support_info.csv'
                    self.request.send(outputname)
                    self.sendfile(outputname)
                    outputname = iname+'/'+iname+'_all.jpg'
                    self.request.send(iname+'_all.jpg')
                    self.sendfile(outputname)
                    outputname = iname+'/'+iname+'_agg.jpg'
                    self.request.send(iname+'_agg.jpg')
                    self.sendfile(outputname)
                    
            except Exception,e:
                print "get error at:",e
                
if __name__ == "__main__":
    host = '145.100.58.60'
    port = 12345
    s = SocketServer.ThreadingTCPServer((host,port), MyTcpServer)
    s.serve_forever()
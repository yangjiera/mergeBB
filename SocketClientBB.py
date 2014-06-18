import socket               # Import socket module
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
s.settimeout(200)
def recvfile(filename):
    print "server ready, now client rece output file~~"
    f = open('client_file/'+filename, 'wb')
    while True:
        data = s.recv(4096)
        if data == 'EOF':
            print "recv output file success!"
            break
        f.write(data)
    f.close()
def sendfile(filename):
    print "server ready, now client sending input file~~"
    f = open('client_file/'+filename, 'rb')
    while True:
        data = f.read(4096)
        if not data:
            break
        s.sendall(data)
    f.close()
    time.sleep(1)
    s.sendall('EOF')
    print "send input file success!"
                                
def confirm(s, client_command):
    s.send(client_command)
    data = s.recv(4096)
    if data == 'ready':
        return True
try:
    s.connect(('145.100.58.60', 12345))
    while 1:
        client_command = raw_input(">>")
        if not client_command:
            continue
                                    
        filename = client_command.split()[0]
        
        if confirm(s, client_command):
            
            
            sendfile(filename)
            
            outputfile = s.recv(4096)
            print "get file:", outputfile  
            if not outputfile:
                print "failed: break the connection!"
                break
            else:
                recvfile(outputfile)
                
            outputfile = s.recv(4096)
            print "get file:", outputfile  
            if not outputfile:
                print "failed: break the connection!"
                break
            else:
                recvfile(outputfile)
                
            outputfile = s.recv(4096)
            print "get file:", outputfile  
            if not outputfile:
                print "failed: break the connection!"
                break
            else:
                recvfile(outputfile)
                
            outputfile = s.recv(4096)
            print "get file:", outputfile  
            if not outputfile:
                print "failed: break the connection!"
                break
            else:
                recvfile(outputfile)
        else:
            print "server get error!"
        
except socket.error,e:
    print "get error as",e
    print s.recv(1024)
finally:
    s.close                     # Close the socket when done
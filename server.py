#!/usr/bin/python
import socket
import sys
import threading
import time
HOSTNAME = 'localhost'
PORT = 3000             # Random port 
BUFFER = 1024

class multiple_clients(threading.Thread):
    def __init__(self,client):
        super(multiple_clients,self).__init__()
        self.client = client

    def receive_data(self):
        try:
            data = self.client.recv(BUFFER)
            return 'Got the message, Thanks..!!'
        except Exception as e:    
            self.client.close()
            return  'Unable to receive the message..!!'

    def send_data(self,data):
        try:
            self.client.send(data)
        except Exception as e:
            self.client.send('Unable to send the data, Check the connection')
            self.client.close()
            return

    def run(self):
        try:
            client_data = self.receive_data()
            if client_data:
                self.client.send(client_data)
        finally:
            pass        
            #self.client.close()      
            
class server_class(threading.Thread):
    def __init__(self):
        super(server_class,self).__init__()
        self.server = None
        self.threads_ = []
         
    def process_data(self):
        client_connection = None                
        print '*'*80
        print 'Server is now running on port %d' % PORT
        print '*'*80

        while True:
            try:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind((HOSTNAME,PORT))
                self.server.listen(10)  # Listen upto 10 connections before droping them (queue).
                client_connection,client_addr = self.server.accept()
                if client_connection:
                    print 'Connection Received from: %s on port: %d' % (client_addr[0],client_addr[1])
                    multiple_cli = multiple_clients(client_connection)
                    #multiple_cli.setDaemon(True)
                    thread_ = multiple_cli.start()
                    self.threads_.append(thread_)
                        
            except Exception as e:
                print '*'*80
                print 'Processing Error..!!'
                print e.message
                print '\nShutting down..!!'
                sys.exit(1)
                raise
                 
            finally:
                self.server.close() 
                #print '*'*80
    def close(self):
        self.server.close()
        
    def run(self):
        self.process_data()

                
if __name__ == '__main__':

    print '*'*80
    print 'Starting Server Daemon..!!'
           
    try:
        server = server_class() 
        server.setDaemon(True)
        server.start()
    except Exception as e:
        print 'Server Stopped'
        print e.message
        print '*'*80
        sys.exit(1)

    try:
        while 1:
            time.sleep(1)
            print 'Enter the command you want to enter:'
            command = raw_input()
            print command
    except Exception as e:
        print e.message
    except KeyboardInterrupt:
        print '*'*78
        print '\nKeyboard Interrupt Caught.!'
        print 'Shutting Down Server..!!!'
        print '*'*80
        sys.exit(1)

    finally:
        server.close()             

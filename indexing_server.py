#!/usr/bin/python
import socket
import sys
import threading
import time
import os

HOSTNAME = 'localhost'
PORT = 3000             # Random port 
BUFFER = 65536

#def get_credentials():
#    cred = socket.socket(socket.AF_INET,)

class multiple_clients(threading.Thread):
    def __init__(self,client):
        super(multiple_clients,self).__init__()
        self.client = client

    def receive_data(self):
        try:
            data = self.client.recv(BUFFER)
            fh = open('./Test/OH_YEAH.pdf','wb')
            fh.write(data)
            return 'Got the message, Thanks..!!'
            fh.close()

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

    # Establish Connection between this peer and the centralized indexing server
    # Get the port number and other credentials from the centralized indexeing server

        
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
        possibilities = [1,2,3]
        print '*'*80
        while 1:
            time.sleep(1)
            print 'Enter your choice.'
            print '1 -  List all the files that are indexed in the CentraliZed Server.'
            print '2 -  Search the file (Returns peer id)'
            print '3 - Current peer statistics\n'
            command = raw_input()
            if int(command) not in possibilities:
                print 'Invalid choice entered, please select again\n'
                continue
            print 'Choice selected: %d \n',int(command)

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

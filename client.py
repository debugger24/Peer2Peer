#!/usr/bin/python
import socket
import sys
from datetime import datetime
import threading
SERVER_HOST = 'localhost'
SERVER_PORT = 3000
BUFFER = 65536

class client_class(threading.Thread):
    def __init__(self,credentials,file_name):
        super(client_class,self).__init__()
        self.client = None
        # This is a tuple (Host_name,Port_addr)
        self.credentials = credentials 
        self.file_name = file_name
        self.output_path = './Test/'
        self.file_size = None

    def write_handler(self,data):
        write_path = self.output_path + self.file_name 
        fh = open(write_path,'wb')
        fh.write(data)
        fh.close()   
    
    def response_handler(self):
        try:
            start_packet_time = datetime.now() 
            raw_data = self.client.recv(BUFFER)
            stop_packet_time = datetime.now()
            write_handler(raw_data)

        except Exception as e:
            print 'Error in receiving or writing data.!!'
            print e.message
            print '*'*80
            self.client.close()
            return
                
        return (stop_packet_time - start_packet_time)
    
    def request_handler(self):
        try:
            start_packet_time = datetime.now()
            data = self.client.send(self.file_name)  
            stop_packet_time = datetime.now()

        except Exception as e:
            print 'Could not receive the data'
            print e.message
            print '*'*80
            self.client.close()
            return
                
        return (stop_packet_time - start_packet_time)
            
    def connect_to_peer(self):
        try:
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client.connect(self.credentials)
            request_time = self.request_handler()
            response_time = self.response_handler()

        except Exception as e:
            print 'Cannot connect to the server..!!'
            print 'Check the connection parameters' 
            print e.message
            print '*'*80
            sys.exit(1)
               
        finally:
            self.client.close()

        print 'Message from the server:', receive_time[0]
        print 'The time taken to receive file:',response_time
        print 'Size of the file transmitted:',self.file_size
        print '*'*80

    def run(self):
        #possibilities = [1,2,3]
        print '*'*80
        try:
            '''
            while 1:
                print '\nEnter the packet size:'
                print 'Enter 1 for 1B'
                print 'Enter 2 for 1KB'
                print 'Enter 3 for 64KB\n'
                option = raw_input()
                if int(option) not in possibilities:
                    print 'Invalid input.!!'
                else:
                    break    
            '''
            fh = open('./Test/PA1.pdf','rb')        
            data_to_send = fh.read() 
            fh.close()
            print '\nNumber of bytes to send:', len(data_to_send)  
            self.process_data(data_to_send,len(data_to_send))

        except Exception as e:
            print 'Error processing the data..!!'
            print e.message
            sys.exit(1)    

if __name__ == '__main__':
    cli = client_class()
    cli.start()
    cli.join() 

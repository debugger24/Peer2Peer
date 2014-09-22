#!/usr/bin/python
import socket
import sys
from datetime import datetime
import threading
SERVER_HOST = 'localhost'
SERVER_PORT = 3000
BUFFER = 1024
SEND_TIMES = []
RECEIVE_TIMES = []

class client(threading.Thread):
    def __init__(self):
        super(client,self).__init__()
        self.client = None
        self.server_addr = (SERVER_HOST,SERVER_PORT)
        # The packet size is varied depending on the user selection
        # Current sizes are 1B, 1KB and 64KB
        self.packet = ['A','A'*1024,'A'*1024*64]
    
    def send_data(self,data):
        try:
            start_packet_time = datetime.now() 
            self.client.send(data)
            stop_packet_time = datetime.now()
        except Exception as e:
            print 'Could not send the data.!!'
            print e.message
            print '*'*80
            self.client.close()
            return
                
        return (stop_packet_time - start_packet_time)
    
    def receive_data(self):
        try:
            start_packet_time = datetime.now()
            data = self.client.recv(BUFFER)  
            stop_packet_time = datetime.now()
        except Exception as e:
            print 'Could not receive the data'
            print e.message
            print '*'*80
            self.client.close()
            return
                
        return (data,(stop_packet_time - start_packet_time))  
            
    def process_data(self,data,packet_size):
        try:
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client.connect(self.server_addr)
            send_time = self.send_data(data)
            receive_time = self.receive_data()
            SEND_TIMES.append(send_time)
            RECEIVE_TIMES.append(receive_time)

        except Exception as e:
            print 'Cannot connect to the server..!!'
            print 'Check the connection parameters' 
            print e.message
            print '*'*80
            sys.exit(1)
               
        finally:
            self.client.close()
        print 'Message from the server:', receive_time[0]
        print 'The time taken to send data:',send_time
        print 'The time taken to receive data:',receive_time[1]
        print 'Packet Size transmitted:',packet_size
        print 'Send Time in microseconds:',send_time.microseconds
        print 'The Bandwidth for the application is %d MBytes/Sec' % (((packet_size/send_time.microseconds)*(pow(10,6)))/(1024 * 1024))
        print '*'*80

    def run(self):
        possibilities = [1,2,3]
        print '*'*80
        try:
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
            data_to_send = self.packet[possibilities.index(int(option))]  
            print '\nNumber of bytes to send:', len(data_to_send)  
            self.process_data(data_to_send,len(data_to_send))

        except Exception as e:
            print 'Error processing the data..!!'
            print e.message
            sys.exit(1)    

if __name__ == '__main__':
    cli = client()
    cli.start()
    cli.join() 

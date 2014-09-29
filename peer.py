from server import server_class
from client import client_class
from FilesystemEventHandler import FilesystemEventHandler
import socket
import sys
BUFFER = 65536

class query_indexer():
    def __init__(self):
        self.ci_server_host = 'localhost'
        self.ci_server_port = 3000
        self.ci_server_addr = (self.ci_server_host,self.ci_server_port)
        self.index_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.index_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.credentials = None
        self.output_dir = './Files/'
        self.LIST_FILES = 'listallfiles'
        self.GET_CREDENTIALS = 'getcredentials'
        self.SEARCH_FOR_FILE = 'searchforfile'

    def send_command_to_cs(self,cmd):
        try:
            self.index_socket.connect(self.ci_server_addr)
            self.index_socket.send(cmd)
            response = self.index_socket.recv(BUFFER)
            return response

        except Exception as e:
            print 'Cannot connect to the Centralized indexing server'
            print e.message
            return 'error'

        finally:    
            self.index_socket.close()         

    def get_credentials(self): 

        try:
            self.credentials = self.send_command_to_cs(self.GET_CREDENTIALS)
            if self.credentials == 'error':
                raise
            self.credentials = int(self.credentials)    
            # Parse the json response and print the options
        except Exception as e:
            print 'Retrive credentials failed'

    def list_all_files(self):
        try:
            all_files = self.send_command_to_cs(self.LIST_FILES)
            # Parse the json response and print the options
        except Exception as e:
            print 'Retrive files list failed'
            print e.message

    def search_for_file(self):
        try:
            search_file = self.send_command_to_cs(self.SEARCH_FOR_FILE)
            # Parse the json response and print the options
        except Exception as e:
            print 'Retrive search file list failed'
            print e.message

    def transfer_file(self,peer_id,file_name):
        try:
            server_addr = ('localhost',peer_id)
            connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            connection.connect(server_addr)
            connection.sendall(file_name)
            response = connection.recv(BUFFER)

        except Exception as e:
            print 'File Transfer failed'
            print e.message

        try:
            file_path = self.output_dir + file_name
            fh = open(file_path,'wb')
            fh.write()
            fh.close()

        except Exception as e:
            print 'Writing binary file failed'
            print e.message

        finally:    
            connection.close()        

    def peer_stats(self):
        print 'Peer Host: localhost'
        print 'Peer Port: %d' % self.credentials

if __name__ == '__main__':

    try:
        qi = query_indexer()    
    except Exception as e:
        print 'Failed to import query package.!'
        print '*'*80
        sys.exit(1) 

    credentials = qi.get_credentials()

    try:
        server = server_class(credentials) 
        server.setDaemon(True)
        server.start()
    except Exception as e:
        print 'Peer Server Could not be started.'
        print e.message
        print '*'*80
        sys.exit(1)

    try:
        fs_handler = FilesystemEventHandler(self.output_dir,credentials)
        fs_handler.setDaemon(True)
        fs_handler.start()
    except Exception as e:
        print 'File system monitor could not be started.'
        print e.message
        print '*'*80
        sys.exit(1)   

    try:
        possibilities = [1,2,3,4]
        print '*'*80
        while 1:
            time.sleep(1)
            print 'Enter your choice.'
            print '1 -  List all the files that are indexed in the Centralized Server.'
            print '2 -  Search the file (Returns peer-id and file size)'
            print '3 -  Get file from peers'
            print '4 -  Current peer statistics\n'
            command = raw_input()
            if int(command) not in possibilities:
                print 'Invalid choice entered, please select again\n'
                continue
            print 'Choice selected: %d \n',int(command)
            if int(command) == 3:
                print 'Enter Peer Id:\n'
                peer_transfer_id = raw_input()
                print 'Enter File name:'
                file_name = raw_input()
                file_name = file_name.lower()

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
from server import server_class
from client import client_class
from FilesystemEventHandler import FilesystemEventHandler
import socket
import sys
import json
import time
BUFFER = 65536
OUTPUT_DIR = './Files/'

'''
1) Things to do, start and stop central indexing server.
2) If a peer goes down, remove all files associalted with the peer in the CS.
3) When entering file name to download, check if it exists in the CS.
4) Same file is getting overriten, is it possible to make a copy?

'''

class query_indexer():
    def __init__(self):
        self.ci_server_host = 'localhost'
        self.ci_server_port = 3000
        self.ci_server_addr = (self.ci_server_host,self.ci_server_port)
        self.index_socket = None
        self.credentials = None
        self.LIST_FILES = json.dumps({'command':'list_all_files'})
        self.GET_CREDENTIALS = json.dumps({'command':'register'})
        self.SEARCH_FOR_FILE = {'command':'search'}

    def send_command_to_cs(self,cmd):
        try:
            self.index_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.index_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.index_socket.connect(self.ci_server_addr)
            self.index_socket.sendall(cmd)
            response = self.index_socket.recv(BUFFER)
            return response

        except Exception as e:
            print 'Cannot connect to the Centralized indexing server'
            print e.message
            return 'error'

        finally:    
            self.index_socket.close()         

    def get_credentials(self): 
        print '*'*80
        print 'Registering peer and fetching credentials from central server\n'
        try:
            self.credentials = self.send_command_to_cs(self.GET_CREDENTIALS)
            if self.credentials == 'error':
                raise
            self.credentials = int(self.credentials)   
            return self.credentials 
        except Exception as e:
            print 'Retrive credentials failed'
            print '*'*80

    def list_all_files(self):
        try:
            all_files = self.send_command_to_cs(self.LIST_FILES)
            all_files_ = json.loads(all_files)
            print '*'*80
            print '\nThe file index list from central server:\n'

            for i,v in all_files_.items():
                print '%s : %s' % (i,map(unicode.encode,v))
            print '*'*80    
        except Exception as e:
            print 'Retrive files list failed'
            print e.message
            print '*'*80

    def search_for_file(self,file_name):
        print '*'*80
        print '\nSearching central file index for the file and peer-id'
        try:
            self.SEARCH_FOR_FILE['filename'] = file_name
            search_command = json.dumps(self.SEARCH_FOR_FILE)
            search_file = self.send_command_to_cs(search_command)
            search_results = json.loads(search_file)
            try:
                print '\nThe File requested are in the following peers:'
                for files_ in search_results[file_name]:
                    print files_,
                print ''
                print '*'*80    
            except:
                print search_results        
                print '*'*80
        except Exception as e:
            print 'Retrive search file list failed'
            print e.message
            print '*'*80

    def transfer_file(self,peer_id,file_name):
        print '*'*80
        print 'Starting File Transfer..!'
        print 'Connecting to peer on:', peer_id
        try:
            server_addr = ('localhost',int(peer_id))
            connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            connection.connect(server_addr)
            connection.sendall(file_name)
            response = connection.recv(BUFFER)
        except Exception as e:
            print 'File Transfer failed'
            print e.message
            print '*'*80

        try:
            file_path = OUTPUT_DIR + file_name
            fh = open(file_path,'wb')
            fh.write(response)
            fh.close()
            print '\nFile Transfer complete'
            print '*'*80
        except Exception as e:
            print 'Writing binary file failed'
            print e.message
            print '*'*80

        finally:    
            connection.close()        

    def peer_stats(self):
        print '*'*80
        print 'Peer Host: localhost'
        print 'Peer Port: %d' % self.credentials
        print '*'*80

if __name__ == '__main__':

    print '*'*80

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
        fs_handler = FilesystemEventHandler(OUTPUT_DIR,credentials)
        fs_handler.setDaemon(True)
        fs_handler.start()
    except Exception as e:
        print 'File system monitor could not be started.'
        print e.message
        print '*'*80
        sys.exit(1)  

    print 'Central Indexing Server is running on port  : 3000'
    print 'This Peer Server is running on port         : %d' % credentials
    print 'Both Central Server and Peer are running on : localhost'    

    try:
        possibilities = [1,2,3,4]
        print '*'*80
        while 1:
            time.sleep(1)
            print '\nEnter your choice.\n'
            print '1 -  List all the files that are indexed in the Centralized Server.'
            print '2 -  Search the file (Returns peer-id and file size)'
            print '3 -  Get file from peers'
            print '4 -  Current peer statistics\n'
            print 'Press cntrl+c to exit.\n'
            command = raw_input()
            if int(command) not in possibilities:
                print 'Invalid choice entered, please select again\n'
                continue
            print '*'*80    
            print 'Choice selected: %d \n' % int(command)

            if int(command) == 3:
                print 'Enter Peer Id:\n'
                peer_transfer_id = raw_input()
                print 'Enter File name:'
                file_name = raw_input()
                file_name = file_name.lower()
                qi.transfer_file(peer_transfer_id,file_name)

            elif int(command) == 1:
                qi.list_all_files()

            elif int(command) == 2:
                print 'Enter File name:'
                file_name = raw_input()
                file_name = file_name.lower()
                qi.search_for_file(file_name)    

            elif int(command) == 4:
                qi.peer_stats()
                    

    except Exception as e:
        print e.message
    except KeyboardInterrupt:
        print '*'*78
        print '\nKeyboard Interrupt Caught.!'
        print 'Shutting Down Peer Server..!!!'
        print '*'*80
        sys.exit(1)

    finally:
        server.close()   
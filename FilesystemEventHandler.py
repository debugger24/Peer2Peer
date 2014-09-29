import sys
import threading
import os
import time
import socket

class FilesystemEventHandler(threading.Thread):
	def __init__(self,monitor_dir,port_id):
		super(FilesystemEventHandler,self).__init__()
		self.cs_indexing_server_addr = ('localhost',3000)
		self.monitor_dir = monitor_dir
		self.files = []
		self.current_directory = './'
		self.port_id = port_id

	def send_notification(self,changes):

		# Changes are now in list format, change them to json response
		try:
        	connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        	connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        	connection.connect(self.cs_indexing_server_addr)
        	connection.sendall(changes)
        	
        except Exception as e:
			print 'Cannot send notification to the server'
			print e.message
			print '*'*80        	

	# Monitor the directory every 1 second and notify the changes 
	# to the centralised indexing server.

	def monitor(self):
		while 1:
			if len(self.files) != 0:
				self.files.sort()
				cur_files = os.listdir(self.current_directory)
				cur_files.sort()
				if cur_files == self.files:
					pass
				else:
					changes = list(set(cur_files) - set(self.files))
					self.send_notification(changes)
			time.sleep(1)		

	def run(self):
		self.monitor()


import sys
import threading
import os
import time
import socket
import json

class FilesystemEventHandler(threading.Thread):
	def __init__(self,monitor_dir,peer_id):
		super(FilesystemEventHandler,self).__init__()
		self.cs_indexing_server_addr = ('localhost',3000)
		self.monitor_dir = monitor_dir
		self.files = []
		self.current_directory = './Test'
		self.peer_id = peer_id
		self.connection = None

	def monitor(self):
		while 1:
			if len(self.files) != 0:
				self.files.sort()
				cur_files = os.listdir(self.current_directory)
				cur_files.sort()
				if cur_files == self.files:
					pass
				else:
					# Make a note of files added and deleted.
					changes_added = list(set(cur_files) - set(self.files))
					changes_removed = list(set(self.files) - set(cur_files))
					changes = (changes_added,changes_removed)
					self.registry(changes,self.peer_id)
			else:
				self.files = os.listdir(self.current_directory)
				self.registry(self.files,self.peer_id)

			time.sleep(1)

	def registry(self,changes,peer_id):
		to_send_ = {peer_id:changes,'command':'index'}
		to_send = json.dumps(to_send_)
		try:
			self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.connection.connect(self.cs_indexing_server_addr)
			self.connection.sendall(to_send)
		except Exception as e:
			print 'Cannot send notification to the server'
        	print '*'*80       

	def run(self):
		self.monitor()

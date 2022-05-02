#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

import socket
import os
import argparse

SEPERATOR = "||"
BUFFER_SIZE = 1024 * 4 

def sendFile(dirname, host, port):
	
	s = socket.socket()
	
	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.")
			#sends dirname & size
	stuff = os.getcwd()
	inStuff = os.listdir(stuff)
	if dirname in inStuff:
		items = os.listdir(dirname)
		for i in range(len(items)):
			pathy = os.path.join(stuff, dirname)
			pathx = os.path.join(pathy, items[i])
			print(pathx)
			filesize = os.path.getsize(pathx)
			s.send(f"{pathx}{SEPERATOR}{filesize}".encode())
			with open (pathx, "rb") as f:
				while True:
					bytesRead = f.read(BUFFER_SIZE)
					if not bytesRead:
						break	#file transmit done
						
					s.sendall(bytesRead)		#assures transmission in busy networks
	s.close()
def main():
	parser = argparse.ArgumentParser(description="Simple File Sender")
	parser.add_argument("dir", help="Directory name to send")
	parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=4891)
	args = parser.parse_args()
	dirname = args.dir
	host = socket.gethostname()
	port = args.port
	sendFile(dirname, host, port)
if __name__ in "__main__":
	main()

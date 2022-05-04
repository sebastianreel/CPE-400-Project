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
	

	#sends dirname & size
	stuff = os.getcwd()
	inStuff = os.listdir(stuff)
	if dirname in inStuff:
		items = os.listdir(dirname)
		for i in range(len(items)):
			pathy = os.path.join(stuff, dirname)
			pathx = os.path.join(pathy, items[i])
			s = socket.socket()
			
			print(f"[+] Connecting to {host}:{port}")
			s.connect((host, port))
			print("[+] Connected.")			
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
	parser.add_argument("directory", help="Directory name to send")
	args = parser.parse_args()
	dirname = args.directory
	host = socket.gethostname()
	port = 4891
	sendFile(dirname, host, port)
if __name__ in "__main__":
	main()

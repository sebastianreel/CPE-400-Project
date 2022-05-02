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

def sendFile(filename, host, port):
	filesize = os.path.getsize(filename)
	
	s = socket.socket()
	
	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.")
	
	s.send(f"{filename}{SEPERATOR}{filesize}".encode())		#sends filename & size
	
	with open (filename, "rb") as f:
		while True:
			bytesRead = f.read(BUFFER_SIZE)
			if not bytesRead:
				break	#file transmit done
				
			s.sendall(bytesRead)		#assures transmission in busy networks
	s.close()

if __name__ in "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Simple File Sender")
	parser.add_argument("file", help="File name to send")
	parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=4891)
	args = parser.parse_args()
	filename = args.file
	host = socket.gethostname()
	port = args.port
	sendFile(filename, host, port)

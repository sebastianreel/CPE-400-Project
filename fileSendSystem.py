#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

import socket
import os
import argparse

SEPERATOR = "<SEPERATOR>"
BUFFER_SIZE = 1024 * 4 

def sendFile(filename, host, port):
	filesize = os.path.getsize(filename)
	
	s.socket.socket()
	
	print(f "[+] Connecting to {host}:{port}")
	s.connect((host, port))
	print("[+] Connected.")
	
	s.send(f "{filename}{SEPERATOR}{filesize}". encode())		#sends filename & size
	
	progress = tqdm.tqdm(range(filename), f "Sending {filename}", unit = "B", unitScale = True, unitAdvisor = 1024)
	
	with open (filename, "rb") as f:
		while True:
			
			bytesRead = f.read(BUFFER_SIZE)
			if not bytesRead:
				break	#file transmit done
				
			s.sendall(bytesRead)		#assures transmission in busy networks
	
	s.close()

if __name__ in "sendFile":
	import argparse
	parser = argparse.ArguementParser(description = "Simple File Sender")
	parser.add_arguement("file", help = "File name to send")
	parser.add_arguement("hose", help = "The host/IP address of the receiver")
	parser.add_arguement("--p", "--port", help = "Port to use, default is 5001", default = 5001)
	args = parser.parse_args()
	filename = args.file
	host = args.host
	port = args.port
	send_file(filename, host, port)

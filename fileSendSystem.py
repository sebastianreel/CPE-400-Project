#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

# import specific libraries from Python to use for the receiving functionality
import socket
import os
import argparse

BUFFER_SIZE = 1024 * 4 
format = "utf-8"

# SENDFILE FUNCTIONALITY
def sendFile(dirname, host, port):
	# get the current directory and the items within it
	cwd = os.getcwd()
	incwd = os.listdir(cwd)
	
	# create a condition: find that the dirname is within the current directory
	if dirname in incwd:
    	# get the items within the directory we are sending data from
		items = os.listdir(dirname)
		
		# loop through the range of the files
		for i in range(len(items)):
    		# connect the path to throughout into the items trhough each iteration of the loop
			pathy = os.path.join(cwd, dirname)
			pathx = os.path.join(pathy, items[i])
			# define the socket
			s = socket.socket()
			
			# show what host name and port that the user is connecting to then connect them
			print(f"[*] Client: Connecting to {host}:{port}...")
			s.connect((host, port))
			print("[+] Client: Connected.")

			# get the filesize of each of the files within the "send" directory
			filesize = os.path.getsize(pathx)
			print(f"[+] Client: File name: '{items[i]}'")
			print(f"[+] Client: File size: {filesize}")
			print(f"[*] Client: Attempting to send file '{items[i]}' to server...")
			s.send(f"Pathway: {pathx} || {filesize} bytes".encode())
			message = s.recv(BUFFER_SIZE).decode(format)
			print(f"[+] Server: {message}.")
			#
			# add code documentation here
			with open (pathx, "rb") as f:
				while True:
					bytesRead = f.read(BUFFER_SIZE)
					if not bytesRead:
						break	#file transmit done
					print(f"[*] Client: Attempting to send file '{items[i]}' data to server...")
					s.sendall(bytesRead)		#assures transmission in busy networks
					dataInfo = s.recv(BUFFER_SIZE).decode(format)
					print(f"[+] Server: {dataInfo}.")
			print("[#]---------------------------------------------------[#]")
	s.close()


def main():
	# parse through the user imput, and if something is not correct, then print said output
	# add an arguement for giving the user information on how to run the program correctly
	parser = argparse.ArgumentParser(description = "Simple File Sender")
	parser.add_argument("directory", help="Directory name to send")
	
	# parse through what the user enters the correct item (in this case a directory name)
	args = parser.parse_args()
	dirname = args.directory

	# gett he host and define the same port id for using in sending files
	host = socket.gethostname()
	port = 4891

	# call the function for sending files nad pass through the directory entered, the host name, and the port id to use in the functionality
	sendFile(dirname, host, port)

if __name__ in "__main__":
	main()
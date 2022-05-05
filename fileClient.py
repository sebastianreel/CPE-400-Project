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
def sendFile(dirname):
	host = socket.gethostname()
	port = 4891
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
			
			# Take the files names withing the clients directory and print them out to see that they are integral and ready to send
			# also take the file size in bytes and print them for integrity checking at the beginning (and end)
			print(f"[+] Client: File name: '{items[i]}'")
			print(f"[+] Client: File size: {filesize}")
			
			# now pritn a statement attempting to send said file to the server
			# then send the socket with the file path and filesize to the server
			print(f"[*] Client: Attempting to send file '{items[i]}' to server...")
			s.send(f"Pathway: {pathx} || {filesize} bytes".encode())

			# the message will look to the server to see if the file was recieved, and then print out what exactly was recieved. 
			# the print for "message" will be found in the server, where the file is specified and sent back over the the client of what sent (basically lets the client know that the file was recieved)
			message = s.recv(BUFFER_SIZE).decode(format)
			print(f"[+] Server: {message}.")
			
			# CASE FOR IF THERE IS DATA IN THE FILE
			# open the file that is conencted to the path directory first
			with open (pathx, "rb") as f:
				# define a loop that will read through the contents of the file after it has been opened
				while True:
					# define a variable defined in bytes that reads the file within the buffersize constraint defined as a global variable
					bytesRead = f.read(BUFFER_SIZE)
					
					# if there isnt anything in the file, then simply stop the loop and close skip to closing the socket
					if not bytesRead:
						break	#file transmit done

					# with data in the file, have a statement confirming that there is an attempt being made to send file data over to the server
					s.sendall(bytesRead)

					# print the message from the recieve to check on the CLIENT side that the file data was recieved. 
					dataInfo = s.recv(BUFFER_SIZE).decode(format)
					print(f"[+] Server: {dataInfo}.")
			print("[#]---------------------------------------------------[#]")
	s.close()


def main():
	# parse through the user imput, and if something is not correct, then print said output
	# add an arguement for giving the user information on how to run the program correctly
	parser = argparse.ArgumentParser(description = "Simple File Sender")
	parser.add_argument("directory", help="Directory name to send")
	#parser.add_argument("files", help="Amount of files to send",default=1)
	# add arguement for multithreading and doing mulitple concurrency or just 1
	#
	
	# parse through what the user enters the correct item (in this case a directory name)
	args = parser.parse_args()
	dirname = args.directory
	#aFiles = args.files

	# gett he host and define the same port id for using in sending files

	# call the function for sending files nad pass through the directory entered, the host name, and the port id to use in the functionality
	print("\t    ===== FILE TRANSFER APPLICATION =====")
	print("[#]---------------------------------------------------[#]")
	sendFile(dirname)
	print("\t    ===== FILE TRANSFER COMPLETE =====")

if __name__ in "__main__":
	main()
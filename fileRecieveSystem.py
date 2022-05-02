#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

import socket

import os


host = socket.gethostname()
port = 4891
buffer = 4096
sep = "||"

s = socket.socket()

s.bind((host, port))

#s.listen(5)
print(f"[*] Listening as {host}:{port}")

c_socket, address = s.accept()
print(f"[+] {address} is connected.")

received = c_socket.recv(buffer).decode()
filename, filesize = received.split(sep)
filename = os.path.basename(filename)

filesize = int(filesize)

with open(filename, "wb") as f:
    while True:
        b_read = c_socket.recv(buffer)
        if not b_read:
            break
        f.write(b_read)
        
currentDirectory = os.getcwd()			#create folder in current directory
directoryName = 'myfolder'
path = os.path.join(currentDirectory, directoryName)
os.mkdir(path) 

c_socket.close()
s.close()

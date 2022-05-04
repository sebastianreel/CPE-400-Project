#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

import socket
import threading
import os


host = socket.gethostname()
port = 4891
buffer = 4096
sep = "||"

s = socket.socket()

s.bind((host, port))

s.listen(10)
print(f"[*] Listening as {host}:{port}")


while True:
    c_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    received = c_socket.recv(buffer).decode()
    filename, filesize = received.split(sep)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    currentDirectory = os.getcwd()			#create folder in current directory
    directoryName = 'myfolder'
    stuff = os.listdir(currentDirectory)
    if directoryName not in stuff:
        path = os.path.join(currentDirectory, directoryName)
        os.mkdir(path)
    else:
        path = os.path.join(currentDirectory, directoryName)
    with open(filename, "wb") as f:
        while True:
            b_read = c_socket.recv(buffer)
            if not b_read:
                break
            f.write(b_read)
    c_socket.close()


        

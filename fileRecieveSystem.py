#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

# import specific libraries from Python to use for the receiving functionality
import socket
import threading
import os

# VARIABLES
# First grab the host computer name to use when identifying what is being listened and connected to
host = socket.gethostname()
# Define a base port to connect to
port = 4891
# The file size amount that the reciever will accept (in bytes)
buffer = 4096
count = 0

# Define a socket, where the system will bind the host to the port and listen constantly
# Then, print out that the server is being listened to, so that that the Send System can successfully work.
s = socket.socket()
s.bind((host, port))
s.listen(10)
print(f"[*] Listening as {host}:{port}")

# RECEIVE FUNCTIONALITY
# run through a loop, this way multiple files can be passed through with one run
while count != 5:
    # after the "fileSendSystem" program has been run, then this loop will be activated
    # the address will be defined and connected to the socket defined before
    c_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    # First, look at what the socket recieved in terms of the directory path and size of the file being moved.
    received = c_socket.recv(buffer).decode()    
    # split the new string into two seperate string lists, with the filename and filesize
    filename, filesize = received.split("||")
    # take the name and only take the final component of the path name, which is a function the "os" library uses.
    # this library is useful for being able to easily connect pathways and parse through directories faster
    filename = os.path.basename(filename)
    # make the filesize, a string within a list of strings, an int instead
    # filesize = int(filesize)
    print("[+] File name: " + filename)
    print("[+] File size:" + filesize)
    
    # get the current directory that the user is on within their current device
    currentDirectory = os.getcwd()
    # name a new directroy where the files are going to be transferred to
    directoryName = 'test_recieve'
    # create a list of strings that shows all of the items in the current directory
    stuff = os.listdir(currentDirectory)
    
    # condition to check that the receive directory is in the current directory
    # join said directroy togetehr so that we can add files into it
    if directoryName not in stuff:
        path = os.path.join(currentDirectory, directoryName)
        os.mkdir(path)
    else:
        path = os.path.join(currentDirectory, directoryName)
    
    #
    # add code documentation here
    with open(filename, "wb") as f:
        joiner = os.path.join(path, filename)

        while True:
            b_read = c_socket.recv(buffer)
            print(b_read)
            if not b_read:
                break
            f.write(b_read)
    c_socket.close()
    
    # iterate upwards and count to the number of files in the directory (5 in this case)
    # set a condition to where the program ends if the number of files has been successfully reached
    count+=1
    if count == 5:
        exit()
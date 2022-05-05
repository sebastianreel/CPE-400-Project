#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

# import specific libraries from Python to use for the receiving functionality
import socket
import os

# VARIABLES
# First grab the host computer name to use when identifying what is being listened and connected to
host = socket.gethostname()
# Define a base port to connect to
port = 4891
format = "utf-8"
# The file size amount that the reciever will accept (in bytes)
buffer = 4096
count = 0

print("\t    ===== FILE TRANSFER APPLICATION =====")


# Define a socket, where the system will bind the host to the port and listen constantly
# Then, print out that the server is being listened to, so that that the Send System can successfully work.
s = socket.socket()
s.bind((host, port))
s.listen(10)
print(f"[*] Server: Listening as {host}:{port}...")
print("[#]---------------------------------------------------[#]")


# RECEIVE FUNCTIONALITY
# run through a loop, this way multiple files can be passed through with one run
while count != 5:
    # after the "fileSendSystem" program has been run, then this loop will be activated
    # the IP address will be defined and connected to the socket defined before
    c_socket, address = s.accept()
    print(f"[+] Client: {address} is connected.")

    print(f"[*] Server: Listening for file...")
    # First, look at what the socket recieved in terms of the directory path and size of the file being moved.
    received = c_socket.recv(buffer).decode()    
    # split the new string into two seperate string lists, with the filename and filesize
    filename, filesize = received.split("||")
    # take the name and only take the final component of the path name, which is a function the "os" library uses.
    # this library is useful for being able to easily connect pathways and parse through directories faster
    filename = os.path.basename(filename).replace(" ", "")
    c_socket.send(f"File '{filename}' recieved".encode(format))
    # make the filesize, a string within a list of strings, an int instead
    # filesize = int(filesize)
    print(f"[+] Client: File name: '{filename}'")
    print(f"[+] Client: File size: {filesize}")
    
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
    
    # CASE FOR IF THERE IS DATA BEING RECIEVED
    # create a joiner variable that joins the path to the filename, so we can view and edit the contents within
    print(f"[*] Server: Attempting '{filename}' file transfer...")
    joiner = os.path.join(path, filename)
    # open the file that is now conencted to the new path that we defined
    with open(joiner, "wb") as f:
        print("[+] Server: File transfer complete.")
        # define a loop that looks at the contents within the file
        while True:
            b_read = c_socket.recv(buffer)
            # if there is no data, stop the loop and move on to close the socket
            if not b_read:
                break
            # if there is data that was in the clients file, write it back into the servers version of the file
            # then send to the client that the data was recieved at the server level
            print(f"[*] Server: Attempting '{filename}' file data transfer...")
            f.write(b_read)
            c_socket.send(f"'{filename}' file data recieved".encode(format))
            print(f"[+] Server: '{filename}' file data transfer complete.")
    print("[#]---------------------------------------------------[#]")
    c_socket.close()
    
    # iterate upwards and count to the number of files in the directory (5 in this case)
    # set a condition to where the program ends if the number of files has been successfully reached
    count+=1
    if count == 5:
        print("\t    ===== FILE TRANSFER COMPLETE =====")
        exit()
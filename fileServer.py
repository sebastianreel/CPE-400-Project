#===========================================================================#
# Authors:  Sebastian Reel, Keegan Graf, Kim Meza Martinez                  #
# Course:   CPE 400: Computer Communication Networks                        #
# Project:  Final Project - Implement a file transfer system                #
# DueL      May 2nd, 2022                                                   #
#===========================================================================#

# import specific libraries from Python to use for the receiving functionality
import socket
import os
import time
import threading
# VARIABLES
# First grab the host computer name to use when identifying what is being listened and connected to
host = socket.gethostname()
# Define a base port to connect to
port = 4891
format = "utf-8"
# The file size amount that the reciever will accept (in bytes)
buffer = 4096
count = 0


# Define a socket, where the system will bind the host to the port and listen constantly
# Then, print out that the server is being listened to, so that that the Send System can successfully work.


# RECEIVE FUNCTIONALITY
# This function will start giving a new thread each time a connection is made.
def threadFunction(c_socket, address):
 
    # the IP address will be defined and connected to the socket defined before
    print(f"[+] Client: {address} is connected.")

    print(f"[*] Server: Listening for file...")
    # First, look at what the socket recieved in terms of the directory path and size of the file being moved.
    received = c_socket.recv(buffer).decode()
    start_time = time.time()    
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
    print(f"[*] Server: Attempting file '{filename}' transfer...")
    joiner = os.path.join(path, filename)
    # open the file that is now conencted to the new path that we defined
    with open(joiner, "wb") as f:
        print(f"[+] Server: File '{filename}' transfer complete.")
        tTime = time.time() - start_time
        print(f"[++] Server: File '{filename}' took {tTime:.7f} seconds to transfer")
        # define a loop that looks at the contents within the file
        while True:
            b_read = c_socket.recv(buffer)
            # if there is no data, stop the loop and move on to close the socket
            if not b_read:
                break
            # if there is data that was in the clients file, write it back into the servers version of the file
            # then send to the client that the data was recieved at the server level
            print(f"[*] Server: Attempting file '{filename}' data transfer...")
            f.write(b_read)
            dTime = time.time() - start_time
            c_socket.send(f"File '{filename}' data recieved".encode(format))
            print(f"[+] Server: '{filename}' file data transfer complete.")
            print(f"[++] Server: File data '{filename}' took {tTime:.7f} seconds to transfer")
    print("[#]---------------------------------------------------[#]")
    c_socket.close()
    
    # iterate upwards and count to the number of files in the directory (5 in this case)
    # set a condition to where the program ends if the number of files has been successfully reached

def main():
    # Makes socket, binds to ip, and listens for files to come in.
    print("\t    ===== FILE TRANSFER APPLICATION =====")
    s = socket.socket()
    s.bind((host, port))
    s.listen(10)
    print(f"[*] Server: Listening as {host}:{port}...")
    print("[#]---------------------------------------------------[#]")
    # Starts multithreading that is used for each socket starting a new connection
    while True:
        c_socket, address = s.accept()
        x = threading.Thread(target=threadFunction, args=(c_socket, address))
        x.start()

if __name__ == "__main__":
    main()
# TCP/IP Socket Requests recognized by Kraken
# D0X0E - Download file             |   D0X0E:MD5_HASH:MD5_HASH:0 (0 bytes downloaded from file)
# D7C00 - Continue downloading file |   D7C00:MD5_HASH:MD5_HASH:X (X = file offset to continue)
# D0X20 - File not found on Peer    |   D0X20

# Required library
import socket
from _thread import *
import time
import hashlib
import os
import sys
import tqdm

# Required modules
from _crypto import EncryptFile


# Read the request file to continue stoped download
def ReadPartFile(Socket_Request, SharedFolderPATH):
	try:
		split_request = Socket_Request.split(':', 3)	# Split the request
		split_file = split_request[1]	# Get the name of requested file
		split_size = split_request[2]	# Get his size
		split_continue = int(split_request[3])	# Get from where file will be downloaded
		thesefile = os.listdir(SharedFolderPATH)	# List the shared files to compare
		for i in thesefile:
			i = SharedFolderPATH + i
			i_char = i
			i_hash = hashlib.md5(i.encode())	# Convert the file name do MD5 Hash
			i_hash = i_hash.hexdigest()
			i_size = os.path.getsize(i)
			i_size = str(i_size)
			i_size_char = str(i_size)
			i_size = hashlib.md5(i_size.encode())	# Convert the file size to MD5 Hash
			i_size = i_size.hexdigest()
			if (i_hash == split_file):	# If the file requested its there, send it!
				return i_char, i_size_char, split_continue
	except:
		pass


def ReadRequestedFile(Socket_Request, SharedFolderPATH):
	try:
		split_request = Socket_Request.split(':', 3)	# Split the request
		split_file = split_request[1]	# Get the name of requested file
		split_size = split_request[2]	# Get his size
		thesefile = os.listdir(SharedFolderPATH)	# List the shared files to compare
		for i in thesefile:
			i = SharedFolderPATH + i
			i_char = i
			i_hash = hashlib.md5(i.encode())	# Convert the file name do MD5 Hash
			i_hash = i_hash.hexdigest()
			i_size = os.path.getsize(i)
			i_size = str(i_size)
			i_size_char = str(i_size)
			i_size = hashlib.md5(i_size.encode())	# Convert the file size to MD5 Hash
			i_size = i_size.hexdigest()
			if (i_hash == split_file):	# If the file requested its there, send it!
				return i_char, i_size_char
	except:
		pass



# Create a new Thread
def newThread(nodeHash, nodeNumber, nodeFolder):
    try:
        while True:
            nData = nodeHash.recv(4096)
            nCommand = nData.decode('utf-8')	# Convert data to UTF-8 char
            if 'D0X0E' in nCommand[:-2]:
                send_file, send_size = ReadRequestedFile(nCommand, nodeFolder) # Get file size and name by TCP request
                nodeNumberStr = str(nodeNumber)	# Get node number
                nodeID = hashlib.md5(nodeNumberStr.encode())	# Convert node number to MD5 hash
                print ('[+] Requested file: ' + send_file + ' [+] Node: ' + nodeID.hexdigest())
                SEPARATOR = '<SEPARATOR>'
                lsock_buffer = 4096	# Size of file that will be sent buffer
                if not os.path.exists(send_file + '.encrypted'):
                    print ('[+] Encrypting file ' + send_file)
                    EncryptFile(send_file)	# Crypt file

                send_file_encrypted = send_file + '.encrypted'	# Inform file name to send it
                send_size_encrypted = os.path.getsize(send_file_encrypted)	# Get the size from crypted file
                progress = tqdm.tqdm(range(int(send_size_encrypted)), f"Sending file ", unit="B", unit_scale=True, unit_divisor=10)
                nodeHash.sendall(f'{send_file_encrypted}{SEPARATOR}{send_size_encrypted}'.encode())	# Send file information TCP/IP Request
                with open(send_file_encrypted, 'rb') as f:
                    while True:
                        bytes_read = f.read(lsock_buffer)
                        if not bytes_read:
                            break
                        nodeHash.sendall(bytes_read)	# Send file by parts to Peer
                        progress.update(len(bytes_read))	# Update progress bar
                    f.close()	# Close file
                nodeHash.close()	# Close socket
            
            
            elif 'D7C00' in nCommand[:-1]:
                send_file, send_size, continue_file = ReadPartFile(nCommand, nodeFolder)
                continue_file = int(continue_file)
                nodeNumberStr = str(nodeNumber)	# Get node number
                nodeID = hashlib.md5(nodeNumberStr.encode())	# Convert node number to MD5 hash
                print ('[+] Requested file: ' + send_file + ' [+] Node: ' + nodeID.hexdigest())
                SEPARATOR = '<SEPARATOR>'
                lsock_buffer = 4096	# Size of file that will be sent buffer
                
                if (os.path.exists(send_file + '.encrypted')):
                    send_file_encrypted = send_file + '.encrypted'	# Inform file name to send it
                    send_size_encrypted = os.path.getsize(send_file_encrypted)	# Get the size from crypted file
                    progress = tqdm.tqdm(range(int(send_size_encrypted - continue_file)), f"Sending file ", unit="B", unit_scale=True, unit_divisor=1024)
                    nodeHash.sendall(f'{send_file_encrypted}{SEPARATOR}{send_size_encrypted - continue_file}'.encode())	# Send file information TCP/IP Request
                    
                    
                    with open(send_file_encrypted, 'rb') as f:
                        f.seek(continue_file)
                        while True:
                            bytes_read = f.read(lsock_buffer)
                            if not bytes_read:
                                break
                            nodeHash.sendall(bytes_read)	# Send file by parts to Peer
                            progress.update(len(bytes_read))	# Update progress bar
                        f.close()
                    nodeHash.close()	# Close socket
                else:
                    nodeHash.send(str.encode('D0X20'))	# Inform Leecher that file was not found!
                    nodeHash.close()
    except:
        nodeHash.close()
        pass


# Get settings to start the Node function
def createNode(nHost, nPort, nLimit, nShare):
    print ('[+] Booting node function')
    time.sleep(1)
    nodeThread = 1  # Specify the number of first thread
    nodeSocket = socket.socket()	# Create a socket relay for node
    nodeSocket.bind((nHost, nPort))	# Bind connection
    nodeSocket.listen(nLimit)	# Wait until nLimit variable connections with Node
    print ('[+] Node created, socket [' + nHost + ':' + str(nPort) + ']')
    print ('[+] Connection limit: ' + str(nLimit))
    print ('[+] Share folder: ' + nShare)
    while True:
        if (nodeThread <= nLimit):
            nodeS, nodeA = nodeSocket.accept()	# Accept connection
            start_new_thread(newThread, (nodeS, nodeThread, nShare))	# Create a new proccess
            nodeThread += 1
        else:
            print ('[+] Limit connection exceeded by node.')
            break
    nodeSocket.close()






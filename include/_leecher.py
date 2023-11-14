# TCP/IP Socket Requests recognized by Kraken
# D0X0E - Download file             |   D0X0E:MD5_HASH:MD5_HASH:0 (0 bytes downloaded from file)
# D7C00 - Continue downloading file |   D7C00:MD5_HASH:MD5_HASH:X (X = file offset to continue)
# D0X20 - File not found on Peer    |   D0X20

# Required library
import socket
import os
import sys
import tqdm
import time

# Required modules
from _crypto import DecryptFile

# Read .kraken file and create parameters to request the file
def ReadFileRequested(rFile, eParameter):
    with open(rFile, 'r') as fContent:
        fLine = fContent.read()
        fLine = fLine[:-1]
        fRequest = 'D0X0E:' + fLine + ':' + eParameter
        return (fRequest)

# Read .kraken file and create parameters inserting file offset to continue download
def ReadContinueRequest(rFile, eParameter):
    with open(rFile, 'r') as fContent:
        fLine = fContent.read()
        fLine = fLine[:-1]
        fRequest = 'D7C00:' + fLine + ':' + str(eParameter)
        return (fRequest)

# Download file function
def DownloadFile(fileRequest):

    # Temporary informations about host to connect
    # must to implement system that will get Peer list hosts to start download

    cHost = '127.0.0.1'
    cPort = 9091
    cFile = fileRequest
    SEPARATOR = '<SEPARATOR>'
    lsock_buffer = 4096

    bRequest = ReadFileRequested(cFile, '0')    # 0 will inform that Leecher don't have any byte of file
    lsock = socket.socket() # Create socket
    print ('[+] Peer found.')
    print ('[+] Connecting to Peer')
    lsock.connect((cHost, cPort))   # Connect to Peer
    time.sleep(1)
    print ('[+] File requested')
    
    lsock.send(str.encode(bRequest))
    received = lsock.recv(lsock_buffer).decode()
    
    if 'D0X20' in received:
        print ('[ERROR] File not found on Peer')
        exit()
    else:
        print ('[+] Request OK')
        
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving file", unit="B", unit_scale=True, unit_divisor=1024)
    
    
    with open(filename, 'wb+') as f:
        while True:
            bytes_read = lsock.recv(lsock_buffer)
            if not bytes_read:
                break
            else:
                f.write(bytes_read)
                progress.update(len(bytes_read))
        f.close()
        lsock.close()
        DecryptFile(filename)


# Continue downloading a file
def ContinueDownload(fileRequest, filePart):

    cHost = '127.0.0.1'
    cPort = 9091
    cFile = fileRequest
    SEPARATOR = '<SEPARATOR>'
    lsock_buffer = 4096
    
    part_file_size = os.path.getsize(filePart)
    bRequest = ReadContinueRequest(cFile, part_file_size)

    lsock = socket.socket() # Create socket
    print ('[+] Peer found.')
    print ('[+] Connecting to Peer')
    lsock.connect((cHost, cPort))   # Connect to Peer
    time.sleep(1)
    print ('[+] File requested')

    lsock.send(str.encode(bRequest))
    received = lsock.recv(lsock_buffer).decode()
    
    if 'D0X20' in received:
        print ('[-] File not found on Peer, please, start download again.')
        exit()
    else:
        print ('[+] Request OK')

    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving file", unit="B", unit_scale=True, unit_divisor=1024)           

    with open(filename, 'ab+') as f:
        while True:
            bytes_read = lsock.recv(lsock_buffer)
            if not bytes_read:
                break
            else:
                f.write(bytes_read)
                progress.update(len(bytes_read))
        f.close()
        lsock.close()
        DecryptFile(filename)


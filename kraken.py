# Kraken: A P2P Crypted Network
# Version: 0.6
# Created by: Mr.Noname (Sockets Archives)
# Required Library: socket, _thread, cryptography, time, hashlib, os, sys, tqdm


# Required library
import sys
import os
import time

# Required modules
sys.path.append('include/')
from _initialization import *
from _node import *
from _leecher import *
from _crypto import GenerateKey
from _crypto import GenerateKrakenFile


# /// Initialization commands ///
if (sys.argv[1] == '--create-node'):    # Node function
    InitFileContent = ReadConfigFile()
    if (InitFileContent == '_File_Not_Found_'): # If configuration file is not found: Default settings
        print ('[ERROR] Configuration file not found, using the default settings.')
        ConfigSettings.nodeHost = '127.0.0.1'   # Local node IP Address
        ConfigSettings.nodePort = 9091  # Local port to receive connections
        ConfigSettings.LimitConnection = 10 # Limit of connection
        if (os.path.exists('share/')):
            ConfigSettings.ShareFolder = 'share/'
            createNode(ConfigSettings.nodeHost, ConfigSettings.nodePort, ConfigSettings.LimitConnection, ConfigSettings.ShareFolder)
        else:
            os.mkdir('share')       # If no exists, create default folder
            ConfigSettings.ShareFolder = 'share/'
            createNode(ConfigSettings.nodeHost, ConfigSettings.nodePort, ConfigSettings.LimitConnection, ConfigSettings.ShareFolder)
    else:   # Read the configuration file content, to set variables
        ConfigSettings.nodeHost = InitFileContent[0]
        ConfigSettings.nodePort = int(InitFileContent[1])
        ConfigSettings.LimitConnection = int(InitFileContent[2])
        if (os.path.exists(InitFileContent[3])):
            ConfigSettings.ShareFolder = InitFileContent[3] + '/'
            createNode(ConfigSettings.nodeHost, ConfigSettings.nodePort, ConfigSettings.LimitConnection, ConfigSettings.ShareFolder)
        else:
            os.mkdir(InitFileContent[3])    # If folder from config file not exists, create it
            ConfigSettings.ShareFolder = InitFileContent[3] + '/'
            createNode(ConfigSettings.nodeHost, ConfigSettings.nodePort, ConfigSettings.LimitConnection, ConfigSettings.ShareFolder)
elif (sys.argv[1] == '--share-file'):
    if (os.path.exists(sys.argv[2])):
        shareFile = sys.argv[2]
        GenerateKrakenFile(shareFile)
    else:
        print ('[ERROR] Wrong path!')

elif (sys.argv[1] == '--download-file'):
    if (os.path.exists(sys.argv[2])):
        downloadFile = sys.argv[2]
        DownloadFile(downloadFile)
    else:
        print ('[ERROR] You must to specify a .kraken file to download')
elif (sys.argv[1] == '--continue-file'):    # Continue downloading a file function
    if (os.path.exists(sys.argv[2]) and os.path.exists(sys.argv[3])):
        krakenFile = sys.argv[2]
        continueFile = sys.argv[3]
        ContinueDownload(krakenFile, continueFile)
    else:
        print ('[ERROR] Specified file not found, please try again.')
elif (sys.argv[1] == '--generate-key'):
    if (sys.argv[2] == ''):
        print ('[ERROR] You must to specify a path and key file to generate it.')
        print ('kraken.py --generate-key /home/user/kraken.key')
        exit()
    else:
        GenerateKey(sys.argv[2])
elif (sys.argv[1] == '--help'): # Read and show Help file message.
    ReadHelpFile()

else:
    print ('[ERROR] Verify your command line, and try again. Or use --help')




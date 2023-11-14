#Kraken: A P2P Encrypted Network   -  Version: 0.1
#Created by: Mr.Injector (Sockets Archives)
                      
                      
    REQUIREMENTS
- Python3+
- Internet Connection
- Linux/Windows/MacOS

      REQUIRED LIBRARIES
- socket 
- os
- sys
- tqdm
- time
- hashlib
- Fernet


      COMMANDS                                
--help            <Show help message>
--create-node     <Start Kraken on Node Mode>
--share-file      <Created a kraken file> <kraken.py --share-file file.pdf>
--generate-key    <Generate a key file to crypt files>
--download-file   <Download a file> <kraken.py --download-file file.kraken>
--continue-file   <Continue stoped download> <kraken.py --continue-file file.kraken file.ext>

    MODULES SPECS                                
_crypto.py
    EncryptFile() - Used to crypt file before send it to the Leech
    DecryptFile() - Used to decrypt downloaded file from Peer
    GenerateKrakenFile() - Read a file to share and generate a .kraken shared file
    GenerakeKey() - Generate a .key file to be used on EncryptFile() and DecryptFile() functions
    
_initialization.py
    ReadConfigFile() - Get informations from <init.conf> file and set parameters to call --create-node COMMANDS
    ReadHelpFile() - Read and show on the screen _help_ file, that contains help commands and Kraken version
    
_leecher.py
    ReadFileRequested() - Interpret .kraken file, generate and return TCP/IP command to request file
    ReadContinueRequest() - Read .kraken unfinished download and generate TCP/IP command to request file
    DownloadFile() - Download file
    ContinueDownload() - Continue an stoped download

_node.py
    createNode() - Peer settings, and request newThread() function
    newThread() - This function generate a new thread to receive multiple socket connections
    ReadRequestedFile() - Read the command line received and read set the file that will be sended to the Leech
    ReadPartFile() - Same as ReadRequestedFile(), but for unfinished download file

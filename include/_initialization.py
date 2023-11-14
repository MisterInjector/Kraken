# Required library
import os

# This class, define initialization variables in case of init.conf was not found
class ConfigSettings:
    def __init__(self, nodeHost, nodePort, LimitConnection, ShareFolder):
        self.nodeHost = nodeHost
        self.nodePort = nodePort
        self.LimitConnection = LimitConnection
        self.ShareFolder = ShareFolder


# Read init.conf content to start node function
def ReadConfigFile():
    if (os.path.exists('include/init.conf')):
        configFile = 'include/init.conf'    # Set configuration file as init.conf
        configRead = open(configFile, 'r')  # Open it in read mode
        configContent = []  # Create an array to receive file content
        for i in configRead:
            i = i.split('=', 4) # Split informations by :
            configContent.append(i[1][:-1])
        return configContent    # Return array with file content
    else:
        return '_config_Not_Found_'

# Read _help_ file content to show help command list
def ReadHelpFile():
    if (os.path.exists('include/_help_')):
        with open('include/_help_') as hFile:
            showHelp = hFile.read()
            print (showHelp)
    else:   # If _help_ is not found, show default command list, without ASCII art
        print ('--help            <Show help message>')
        print ('--create-node     <Start Kraken on Node Mode>')
        print ('--share-file      <Created a kraken file> <kraken.py --share-file file.pdf>')
        print ('--generate-key    <Generate a key file to crypt files>')
        print ('--download-file   <Download a file> <kraken.py --download-file file.kraken>')
        print ('--continue-file   <Continue stoped download> <kraken.py --continue-file file.kraken file.part>')
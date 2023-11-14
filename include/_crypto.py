from cryptography.fernet import Fernet
import hashlib
import os
import sys
import time

# Encrypt File Function
def EncryptFile(FileToEncrypt):
	try:
		with open('include/kraken.key', 'r') as read_hash:	# Open file with Base64 Hash key
			base64_hash = read_hash.read()	# Read his content
			fernet = Fernet(base64_hash)	# Create object to crypt the file content
		with open(FileToEncrypt, 'rb') as f:
			original_file = f.read()	# Get original file content
			encrypted_file = fernet.encrypt(original_file)	# Encrypt the content

		with open(FileToEncrypt + '.encrypted', 'wb') as cfile:
			cfile.write(encrypted_file)	# Save a new file crypted
	except:
		print ('[+] Error to encrypt file.')


# Decrypt File Function
def DecryptFile(FileToDecrypt):
	with open(FileToDecrypt, 'rb') as df:
		encrypted_content = df.read()
	try:
		with open('include/kraken.key', 'r') as get_key:	# Open file with Base64 Hash key
			the_password = get_key.read()	# Read his content
			fernet = Fernet(the_password)	# Create object to decrypt the file content
			decrypted_content = fernet.decrypt(encrypted_content)
			explode_file_name = FileToDecrypt.split('.', 3)	# Split file.extension.encrypted
			save_to_file = explode_file_name[0] + '.' + explode_file_name[1] # Set new name to file.extension
		with open(save_to_file, 'wb') as lf:
			lf.write(decrypted_content)		# Save decrypted file
			os.remove(FileToDecrypt)	# Delete encrypted file
	except:
		print ('[+] Fail to decrypt downloaded file.')	


# Generate .kraken file
def GenerateKrakenFile(gFilePath):
	try:
		print ('[+] Generating file\t', end ='')
		time.sleep(1)
		file_path = gFilePath	# Set file PATH
		file_size = os.path.getsize(file_path) # Get size of file in bytes
		file_size = str(file_size)	# Convert bytes in String
		file_hash = hashlib.md5(file_path.encode())	# Convert file name to MD5 Hash
		file_hash = file_hash.hexdigest()	# Convert MD5 to hexadecimal value
		size_hash = hashlib.md5(file_size.encode())	# Convert file size to MD5 Hash
		size_hash = size_hash.hexdigest()	# Convert MD5 to hexadecimal value
		kraken_name = os.path.basename(file_path) + '.kraken'	# Generate a name for kraken file
		kraken_hash = hashlib.md5(kraken_name.encode())	# Convert it to a MD5 Hash
		kraken_hash = kraken_hash.hexdigest()	# Convert MD5 to hexadecimal value

		with open(kraken_hash + '.kraken', 'a+') as cFile:
			cFile.write(file_hash + ':' + size_hash)
			cFile.close()
			print ('OK')
			print ('[+] File generated: ' + kraken_hash + '.kraken')
	except:
		pass


# Generate .key file
# DISCLAIMER: If you generate another .key file and use it on your P2P Network, Leechers
# will don't be able to download your files anymore, except if they have the new generated key

def GenerateKey(keyPath):
    try:
        generatedKey = Fernet.generate_key()
        with open(keyPath, 'w') as f:
            f.write(str(generatedKey))
            f.close()
            print ('[+] Generated key: ' + str(keyPath))
    except:
        print ('[ERROR] Fail to generate key')

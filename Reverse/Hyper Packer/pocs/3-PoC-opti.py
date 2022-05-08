#!/usr/bin/python3
from Crypto.Cipher import AES
import itertools

# SETTINGS

PACKED_OFFSET_BEGIN = 0x2600
PACKED_OFFSET_END   = 0x2650
IV_OFFSET           = 0x48E80

# 1 - KEY GENERATION FUNCTIONS

def bitwise_not(numBin):
    numBinNegated = ""
    for i in numBin:
        if i=='1':
            numBinNegated += "0"
        else:
            numBinNegated += "1"
    return numBinNegated

def generatePossibleKeys(IV):
    # For each byte of IV, we bruteforce corresponding possibilities of byte for the key
    possibilities = []
    n = 0
    for i in range(0, 16):
        possibilities.append([])

        # OBSERVATION: if a byte of IV == 0, corresponding byte of key will be always == 0 too!
        if IV[i] == 0:
            possibilities[n].append(0x0)

        # Byte generation process
        else:
            for bKey in range(0,255):
                bIVnot = int(bitwise_not(bin(IV[i])), 2)
                if bKey & bIVnot == 0:
                    possibilities[n].append(bKey)
        n+=1

    # Generating all possibilities of keys using itertools.product which greatly does the job for us!
    possibleKeys = [] # returned as byte array
    for possKey in itertools.product(*possibilities):
        keyHex = ""
        for nb in possKey:
            keyHex += "{:02x}".format(nb)
        possibleKeys.append(bytes.fromhex(keyHex))

    print("[*] Number of possible keys:", len(possibleKeys))
    return possibleKeys

# 2 - DECRYPTION FUNCTIONS

def decryptCbc(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    original_data = cipher.decrypt(data), AES.block_size

    return original_data[0]

# 3 - CORE FUNCTIONS

def parseSecret(data):
    index = data.find(b"SECRET is : ")
    secret = data[index+12:index+50] # read large amount of data just in the case where length of secret would change
    secret = secret[:secret.find(b'\0')] # then remove nullbytes at the end
    return secret

def decryptPackedFile(filename):
    with open(filename, "rb") as f:
        # Read packed data
        f.seek(PACKED_OFFSET_BEGIN, 0)
        packed = f.read(PACKED_OFFSET_END - PACKED_OFFSET_BEGIN)

        # Read IV
        f.seek(IV_OFFSET, 0)
        iv = f.read(16)
        print("IV:", iv)
    
    keys = generatePossibleKeys(iv)

    # Read the IV for decryption at offset 0x0x25F0!!!
    with open(filename, "rb") as f:
        f.seek(0x25F0, 0)
        iv2 = f.read(16)
    
    for key in keys:
        decrypted = decryptCbc(key, iv2, packed)
        
        # check if it's indeed the unpacked data we're looking for!
        if decrypted[:4] == b"Take":
            print("[+] Successfully decrypted the packed MZ-PE!")
            print("[+] Correct key was", key)
            return decrypted

    # if we reach this point, we didn't found the correct key
    print("[-] All key candidates tested, couldn't decrypt the packed MZ-PE :(")
    return 0

# Main

# Decrypt the file
decryptedMzPe = decryptPackedFile("packed.bin")
with open("unpacked.bin", "wb") as f:
    f.write(decryptedMzPe)
print("[+] File extracted to 'unpacked.bin'")

# Search the secret
secret = parseSecret(decryptedMzPe)
print("[\o/] Found secret:", secret.decode('utf-8'))

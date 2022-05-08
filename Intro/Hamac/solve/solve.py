### Requirements: pip3 install pycryptodome

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import HMAC, SHA256

# Read password candidates in rockyou.txt
with open("/path/to/your/rockyou.txt :)", "rb") as f:
    passwords = f.readlines()

# IV and encrypt data present in output.txt
iv = bytes.fromhex("ea425b2ea4bb67445abe967e3bd1b583")
encrypted = bytes.fromhex("69771c85e2362a35eb0157497e9e2d17858bf11492e003c4aa8ce1b76d8d3a31ccc3412ec6e619e7996190d8693299fc3873e1e6a96bcc1fe67abdf5175c753c09128fd1eb2f2f15bd07b12c5bfc2933")

# Bruteforce loop
for psw in passwords:
    
    # Key generation
    password = psw[:-1]
    h = HMAC.new(password, digestmod = SHA256)
    h.update(b"FCSC2022")
    k  = SHA256.new(password).digest()

    # Decrypt
    try:
        cipherObj = AES.new(k, AES.MODE_CBC, iv = iv)
        cleartext = unpad(cipherObj.decrypt(encrypted), AES.block_size).decode()

        print("[+] Well done, flag decrypted with key %s! Flag is:" % (psw))
        print(cleartext)
        exit(0)
    except:
        continue

# Finally: flag is FCSC{5bb0780f8af31f69b4eccf18870f493628f135045add3036f35a4e3a423976d6}!

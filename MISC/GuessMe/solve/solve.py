#!/usr/bin/python3

from pwn import *

p = remote("challenges.france-cybersecurity-challenge.fr", "2001")
N = 64

for _ in range(0, 16):
    rnge = [0, pow(2, N)-1]
    
    # Dichotomy stuff
    for i in range(0,N+1):
        middle = int(rnge[0] + int((rnge[1]-rnge[0])/2))
        print("Inf %d sup %d / middle %d" % (rnge[0], rnge[1], middle))

        p.sendline(str(middle).encode())
        out = p.recvline()
        print(out)

        # on est en dessous du nombre à deviner
        if out == b'>>> +1\n':
            rnge = [middle, rnge[1]]
            
        # on est au dessus
        elif out == b'>>> -1\n':
            rnge = [rnge[0], middle]

        # on l'a deviné
        else:
            print("Guessed it!")
            print(p.recvline())
            break

    if i == N:
        print("[-] Error: couldn't guess it :(")
        exit(-1)

print("Flag:", p.recvline())

# Flag is: FCSC{7b20416c4f019ea4486e1e5c13d2d1667eebac732268b46268a9b64035ab294d}

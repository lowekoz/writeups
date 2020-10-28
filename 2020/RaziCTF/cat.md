ssh catFlag@37.152.181.193
password is:r34lly34syp@55

connect, do ls and notice that there's a flag.txt, but only a few allowed commands and "cat flag.txt" prints something else.
Assume that flag.txt actually contains flag but something weird is going on, so instead of connecting to the remote server I just run the command "cat flag.txt" remotely, so that the output is printed unmodified on my own machine. This is done with ```ssh catFlag@37.152.181.193 cat flag.txt```, and sure enough after giving the password, the flag is printed.

#RaziCTF{th3r3_!s_4_c4t_c4ll3d_fl4g}.
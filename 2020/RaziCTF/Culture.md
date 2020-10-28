Given a png with the description "This chall is not significant!!!", hints towards a LSB (Least Significant Bit) manipulation
of the picture such that if we read the LSB from each color for each pixel and and concatenate thoose bits, we get the message.
More on: https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372

However, the the LSB of RGB was meant to be read in order BGR, because Arabic.

```py
from PIL import Image
p = r'C:\Users\lowek\Documents\CTF\Culture\enc.png'
im = Image.open(p,)
pix_val = list(im.getdata()) #extract pixels into list
ANS = ""
n = 8
bb = ""
for el in pix_val:
    b = bin(el[-1])[-1] #B
    b += bin(el[1])[-1] #G
    b += bin(el[0])[-1] #R
    
    bb += b

bb += "0" * (n-(len(bb)%n)) #padding in case it was needed

for i in range(0,len(bb)-n,n): #interpret as ASCII foreach byte
    tmp = ""
    for j in range(i,i+n):
        tmp += bb[j]
    #readable chars
    if  int(tmp,2) <= 127 and int(tmp,2) >= 33:
        ANS += chr(int(tmp,2))
    tmp = ""

with open(r"C:\Users\lowek\Documents\CTF\Culture\out.txt",'w') as f:
    f.write(ANS)

#RaziCTF{i_s33_ur_4_MaN_0f_LSB_aS_W3LL}=====Im$I$JI$mmI$...
```

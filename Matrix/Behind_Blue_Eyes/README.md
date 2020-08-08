> ### Behind Blue Eyes
> Not everything meets the eye

'Behind Blue Eyes' challenge was under 'warmup' category and worth 20 points.  
A zip file was attached to the challenge, consists of 12 photos of a blue eye.  
While unpacking, I already noticed that all of the pictures have the same size but different CRCs, which means that the files are different:  

![The rar archive](/Matrix/Behind_Blue_Eyes/images/rar-CRC.png)

Needless to say that the photos look the same by eye.  

To see the difference between the files we can use the CMD command `fc`(file comparison):  
![fc command](/Matrix/Behind_Blue_Eyes/images/fc-command.png)

Bullseye, now we know the steganography method that had been used - only 1 byte in offset 0x50(found by using the /b parameter).  
Well, we can now decide whether to compare each picture using the `fc` command manually, OR use a python script to automatically find the flag...  
Of course I would choose the second option :upside_down_face:
 
```python
flag = ''
for i in range(12):
    with open("./Photos/" + str(i) + ".jpeg", "rb") as image:
        b = bytearray(image.read())
        flag += chr(b[0x50])
print(flag)

# FLAG_THE_WHO
```

__Flag:__ `FLAG_THE_WHO`

> ### xor-with-xor
> We found this file on an evil hacker's computer. It's probably encrypted, but we don't know how to decrypt it.  
> We need your help!  
> Thanks in advance :)

'xor-with-xor' challenge was under 'Misc' category and worth 30 points. A file named `xor-with-xor.bin` was attached to the challenge.  
The fact that the file had no magic number and the name of the challenge (and the file) included xor, brought me to the conclusion that the file is encrypted with xor.  
But what is the key?... Well, that's pretty easy - the name reveals that it's "xor with xor" encrypted :)  
I can either use the easy way to xor with an hex editor like 'Neo hex editor' or the free 'wxHexEditor', OR I can write a python script...  
Of course I would choose the second option :upside_down_face:

```python
key = [ord(char) for char in 'xor']  # [120, 111, 114]
with open('xor-with-xor.bin', "rb") as file_handler:
    cipher = bytearray(file_handler.read())

plain_text = bytearray()
i = 0  # i is being used to determine the index in the key for each iteration of the decryption.
for byte in cipher:
    plain_text.append(byte ^ key[i % 3])
    i += 1

with open('decrypted-file', "wb") as file_handler:
    file_handler.write(plain_text)

print("First five values are: {}".format(plain_text[:5]))
# First five values are: bytearray(b'PK\x03\x04\x14')
```

The first four bytes are `50(P) 04(K) 03 04` which is the magic number of zip file. Once I open the zip file I see a list of 1,000 compressed files:

![The ZIP](/Checkpoint/xor_with_xor/images/zip_files.png)  

The files' names start with 0.dat and ends with 999.dat, in a following order. It is clear that the original file was divided to the 1,000 files that we see here.  
Concatenating them should be a super easy task - in bash we only use `cat {0..999}.dat > original.dat`  

But then it would be easy, too easy :) The challenge here is a bit more complex - some of the filenames are mixed with some chars like `1|7|8.dat`, `9$8$6.dat`, `2x3x3.dat` and more. Hence we first need to get rid of these junk characters and then we can merge the files.  
```python
import os
from sys import platform

files_list = os.listdir('./decrypted_file')  # Gets a list of files names in the zip's .
for file_name in files_list:
    for char in "|$ [xT_":
        if char in file_name:
            new_name = file_name.replace(char, '')
            os.rename('./decrypted_file/' + file_name, './decrypted_file/' + new_name)
            break # Each file has only 1 kind of special char.

# Merge the files to 'original.dat' file
if platform.startswith('linux'):  # Old python versions might have different platform name for linux kernel versions such as linux2
    os.system("cat ./decrypted_file/{0..999}.dat > ./decrypted_file/original.dat")

```

Now we have the original-merged file. A short examine with hex editor and I see that this file's type is GZIP(magic numbers `1f 8b`).  
Decompress and... We get a `WAV`(audio) file with a woman reading the flag.


__Flag:__ `csa{you_are_a_very_good_listener}`

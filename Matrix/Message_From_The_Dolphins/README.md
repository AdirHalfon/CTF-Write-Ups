> ### Message From The Dolphins
> The Zip got crumbled and the massage got scrambled.
> Capture the flag to get the message from the Dolphins.


'Message From The Dolphins' challenge was under 'other' category and worth 70 points.  
A file named '42'(the dolphins want to tell us the meaning of life? :)) attached to the challenge, probably a zip file(as the description hints).  
Just to make sure:

![Hex of 42 shows zip magic number](/Matrix/Message_From_The_Dolphins/images/magic_number.png)  
_Indeed a zip file._

But when we try to decompress the archive we get a warning says the archive is corrupted:

![Archive warning](/Matrix/Message_From_The_Dolphins/images/archive_corrupted.png)  
_Notice the size of the packed file. Definitely shouldn't be 0_

A short study of the 'zip' file structure, teaches that at offset 0x12 of the local file header and at offset 0x14 of the central directory header should be the file compressed size.  
To calculate the compressed size, I used the free trial of 'Hex Editor Neo' which is very powerful hex editor, containing a lot of features such as bookmarking and binding file structures.  
When I've bound the zip file structure I immediately noticed that the extra field length is not correct.  
So I simply removed the extra field and changed it's length to 0 :)  
The extra field is not necessary at all and to avoid other problems with it we can just remove it.  
To calculate the compressed size, I selected the header and the footer and then chose inverse select.  
There are couple more fields to fix(such as header's offset), but at this point we can use WinRAR's built-in repair tool(ALT+R) to fix it faster for us. After we fix the corrupted zip, we can decompress the image inside it:

![The decompressed image](/Matrix/Message_From_The_Dolphins/images/message_from_dolphins.png)  
_Another steganography challenge, huh? :)_

This time we only have 1 image, in contrast to the first challenge that we had 12 images so it's clear that we are now facing another method of steganography.  
LSB(least significant bit) is the most common method - in which we change the least significant bit of each byte(on each color component, for RGB there are 3 per pixel) according to the data we want to hide.  
We can test our theory with free online steganography services, OR we can write a python script to do it...  
Of course I would choose the second option :upside_down_face:

```python
from PIL import Image

img = Image.open('images/message_from_dolphins.png')
pixels = list(img.getdata())
flag_byte = 0
flag = ''
for i in range(len(pixels)):
    # Each pixel has 3 color components and a alpha which is not relevant for us(RGBA), thus our loop iterates 3 times.
    for j in range(3):
        bit = (pixels[i][j] % 2)  # In LSB method, an even number is a 0 in the original text whereas an odd is 1.
        bit_number = (i * 3 + j) % 8  # This variable stores the bit number in the current byte.
        flag_byte += bit << (7 - bit_number)  # To make sure each bit gets its right place by shifting.
        if bit_number == 7:  # If the current bit is the eighth - it means we finished a byte.
            flag += chr(flag_byte)
            flag_byte = 0

print(flag)

```

The algorithm is very simple - first we get the list of the pixels using PIL module. Due to the color model of the image, which is RGBA, each pixel is actually a tuple of 4 integers.  
The forth(Alpha) is not relevant and is not being used here, therefore we iterate 3 times over each pixel, check each color component's value whether is odd or even and add it to flag_byte in the correct position using shifting.  
When we get to the eighth bit we translate the byte we got to a char and add it to the flag string.

__Flag:__ `Flag_So_long_and_thanks_for_all_the_fish`

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

flag = ''
for i in range(12):
    with open("./Photos/" + str(i) + ".jpeg", "rb") as image:
        image_bytes = bytearray(image.read())
        flag += chr(image_bytes[0x50])  # 0x50 is the offset from the beginning of the file which changes among the photos and consists the flag.
print(flag)

# FLAG_THE_WHO

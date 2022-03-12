key = [ord(char) for char in 'xor']  # [120, 111, 114]
with open('xor-with-xor.bin', "rb") as file_handler:
    cipher = bytearray(file_handler.read())

plain_text = bytearray()
i = 0  # i is being used to determine the byte of the key for each iteration of the decryption.
for byte in cipher:
    plain_text.append(byte ^ key[i % 3])
    i += 1

with open('decrypted-file', "wb") as file_handler:
    file_handler.write(plain_text)

print("First five values are: {}".format(plain_text[:5]))
# First five values are: bytearray(b'PK\x03\x04\x14')

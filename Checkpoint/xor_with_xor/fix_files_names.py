import os
from sys import platform

files_list = os.listdir('./decrypted_file')  # Gets a list of files names in the zip's .
for file_name in files_list:
    for char in "|$ [xT_":
        if char in file_name:
            new_name = file_name.replace(char, '')
            os.rename('./decrypted_file/' + file_name, './decrypted_file/' + new_name)
            break

# Merge the files to 'original.dat' file
if platform.startswith('linux'):  # Old python versions might have different platform name for linux kernel versions
    os.system("cat ./decrypted_file/{0..999}.dat > ./decrypted_file/original.dat")

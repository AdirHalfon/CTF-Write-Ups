> ### Somewhat SecureBoot
> My boss told me to implement a chain of trust mechanism for a remote server boot process. He said: "There are 3 bootloaders - BL1, BL2, BL3. make sure that no one will be able to compromise our images. use a strong integrity solution, You can use SHA256 or something."  
> So that's exactly what I did. The funny thing is - BL3 was already compromised, I have no idea what BL3 is suppose to do. But I do know that it's something important.  
> BTW, I don't think my boss knows much about integrity (don't tell him I said it).  
> nc challenges.ctfd.io 30071


'Somewhat SecureBoot' challenge was under 'PWN' category and worth 150 points.  
To find the flag, we firstly have to connect to the remote server with 'netcat'. Once connected, we are asked to enter an input and this is what we get:

![Output upon connection](/Matrix/Somewhat_SecureBoot/images/connection.png)  
_Notice the hash of BL3.bin, one line above the "expected hash"_

Uhm... We get an error message saying that to load bootloader 3 it was expecting for 64 times 'a' as the hash. So I tried to enter 64 times 'a' as an input and I got another error message saying it was expecting for 32 times 'a'. Let's try it again - I enter 32 times 'a' and this time the error says it was expecting for (Nothing) as a hash. Strange!

So I tried some more manual fuzzing until I noticed that everything I write after the 32nd character is shown as the expected hash. Interesting! It seems like we are on the right way!  
We do know the hash of bootloader3 file(which is the correct hash it should be expecting for). What if we put 32 junk chars, and then the real hash?... Will it expect for the correct hash like it should?

![Output with flag](/Matrix/Somewhat_SecureBoot/images/bootloader3.png)  

Well, it worked! 

__Flag:__ `FLAG__b00t_c0mpleted`

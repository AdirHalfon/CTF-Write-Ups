> ### Fly Me To The Moon
> Our Satellite managed to pick up some data from outer space (Aliens? wink wink).  
> We have tried to make some sense of it for a long time, Maybe you can? It's a new year after all...

'Fly Me To The Moon' challenge was under 'forensics' category and worth 85 points.  
A file with no suffix was attached to the challenge similarly to 'Message From The Dolphins' challenge, but this time no luck determining the file type - it has no magic number.  
So I tried to search for any legitimate string might be in it, and I noticed that all of the strings are either 55 or 4 characters long, except to one!  
The only string that was neither 55 nor 4 chars long was `RkxBR19CUklOR19CQUNLX1NJTkFUUkE=`. Uhm... This format looks familiar...

![Strings output](/Matrix/Fly_Me_To_The_Moon/images/strings.png)  

This string is base64 encoded(as the '=' suffix hints). To decode it we can use free online services such as CyberChef OR we can write on our own an extremely short python script...  
Of course I would choose the second option :upside_down_face:

```python
import base64
flag_bytes = base64.b64decode('RkxBR19CUklOR19CQUNLX1NJTkFUUkE=')
flag = flag_bytes.decode()
print(flag)
```

Well, this one was easy.  
__Flag:__ `FLAG_BRING_BACK_SINATRA`

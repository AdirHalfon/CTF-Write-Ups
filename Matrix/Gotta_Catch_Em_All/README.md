> ###  Gotta catch em all  
> Ash was too busy catching pokemons that he forgot his credentials.  
> https://ashmatd.herokuapp.com/  
> Please don't use brute force or a scan of any kind, it will not get you closer to the solution.  


'Gotta catch em all' challenge was under 'Web' category and worth 80 points.  
In this challenge we have a URL to ash's site. This site has 5 pages (including the home page), which 3 of them are static.

![The home page and the menu](/Matrix/Gotta_Catch_Em_All/images/homepage.png)  
_The home page, "About me" and "Pictures" seem to be static pages, thus irrelevant._

The only interesting pages are the Login form and "Contact me".  

By the description, we can take an educated guess that neither brute-forcing nor scanning the site would work :)  
Therefore, I started by fuzzing the contact page. In the beginning I tried XSS to steal the admin's cookie which did not work, then I tried (manually) SQLi on the login page that did not work as well.  
During the XSS attempts I noticed a server error that reveals information about the implementation of the server!  
The error was caused because of an exception that raised because the title was too long.

![The relevant code from the contact page](/Matrix/Gotta_Catch_Em_All/images/contact_error.png)  
_some text_

Now we know (well partly, but sufficient) what happens when we send a message to contact Ash! It appends (or creates, if does not exist) a file named as the title with `txt` extension in the directory `messages/`.  
OK but... How does it help us? We have to dig deeper. So I tried to provide long credentials, hoping that we will get another error page that will reveal additional back-end code:

![The relevant code from the login page](/Matrix/Gotta_Catch_Em_All/images/login_error.png)  
_some text_

The login page reads a file located in `private/accounts.txt` which acts as the database of the site. Each account is a line in the format `{username}: {password}`.  
Awesome! All we have to do is to add an account using the contact page, and then to log in.  
As we already mentioned, the title is used to determine the file that will be appended by the content of the body, which should be the credentials in the correct form. Thus our contact will look like this:

![contact page payload](/Matrix/Gotta_Catch_Em_All/images/payload.png)  

And then we can log in and get the flag:  

![The flag! Wohoo!](/Matrix/Gotta_Catch_Em_All/images/flag.png)  

__Flag:__ `FLAG_aSh_Ketchup`

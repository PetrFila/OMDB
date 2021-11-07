Hi Petr,

I like the general structure.  You put some work into the README.md, which is nice.

Comments:
1. I hit the same problem as Luke:
    from .api_key import omdb
ModuleNotFoundError: No module named 'search.api_key'

This means that the api_key doesn't exist.  Apart from giving instructions for how to create one, I'd also suggest wrapping this import in a try block, to give the user a nice error message and possibly instructions at runtime for how to create an api_key.

I got it running, but had to both debug your code, and look at the requirements doc. It was easier for Luke, as he knew the requirements.

2. You added "*.pyc" to your .gitignore, which is great.  Unfortunately you did it after checking in some .pyc files.  You can remove them individually or with a command like:
find . -name "*.pyc" -exec git rm -f "{}" \;
Just be careful where you run that from!

3. I loved that your error messages were displayed on the search screen.  It meant I didn't need to use the back button, nice touch.

4. It would have been nice if your search results also contained a "back" link, or better yet just below the search screen.

5. As you included the database, you should have included the username/pass in the README.  Or better to just let the user create the database from a script.

6. Small things:  Your code could use some comments. Remove the print statement. Add some logging (if it was in a bigger project). Use caps for constants. Django views can use functions or classes.  The classes come in handy when you have many views, so you can use inheritance to remove some repetition.  I would have used a function in this small project too though.  :)

7. Oh, I forget, in the README I first did a “git clone” command, and then a “cd omdb” before the “piping shell” command.  I didn’t want to create the Pipfile in my ~/project dir.

8. Functionally, great work!


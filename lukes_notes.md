# Luke's notes for Petr Fila's OMDB task

## Setup and running without inspecting code

1. It is good practise to add a `requirements.txt` file to the project. This file is a simple text file with a python package requirement on
   each line. Then instead of having to advise which packages to install, one can simple say to install the requirements file.
   ```bash
   pip install -r requirements.txt
   ```
   I have added the requirements file in this Pull request that could be used for this project. 
2. Nice touch to not include the API key in the repository. 
3. There are no instructions for how to get project to work when there is no API key present. It's generally a good idea
to be helpful wherever possible. I put an exmple of how you might approach that through catching an import error.
4. An SQL Lite Database is included in the repository. This can cause a bit of chaos in multi user situations. 
   It may have been better to not include the database in the repo to add a step in the instructions letting 
   users know to build their local SQLite database
   ```bash
    python manage.py migrate
    ```
   
I got up and running okay, but I am a very technical audience. As a test plan, it is better to hold more hands than give
pushes into the wilderness. 

## Interacting with the service

1. One that becomes clear immediatly is that I only ever get one result regardless of the search terms, types or other 
combinations I used. I thought this may have been because the repo database had data in it and so you only show the
   local results, but clearing the database and starting again still only gives a single  result. 
   
   **Note** It looks like OMDB API has been crippled to only ever return a single result. The page parameter doesn't even work. 
   
2. The problem with the results aside, it seems to work okay. 
3. The Django admin site doesn't load CSS by default. You can set the project settings DEBUG=False to have django
serve the static files for you in development.
4. Admin site loaded up okay and can see that it's been configured to work with vanilla settings. Django admin is incredibly powerful so
it would be a good idea to play around with that when you can. 
   
## Testing plan

The testing plan itself is good. It contains a good overview of what inputs should produce what outputs. 

I see you're picking up the Aussie lingo.
```
Nah, sorry mate. There is no such a title in the database.
Sorry mate. GET method is not allowed.
Sorry mate. Movie not found!
Sorry mate. Connection Error to the external API
```

## The code itself

### The positives

1. Demonstrated that you are able to build an application that mostly meets a spec
2. In order to do this you had to learn how to interact with a new 3rd party API
3. You also had to find out how to create an application using Django, an application that I know you have not much experience in (if any at all)
4. It's a solid start and shows that you've got the makings of a dev in you. 

### The room to improve

1. Your inexperience does show, but that's not unexpected. You are used to writing procedural scripts that run top to  bottom and exit. Thinking in objects and 
classes as part of a larger application is something that comes with experience and you'll pick it up. The MW team is always willing to help develop good practices and 
   code review is very important to us. 
2. It would be nice for you to have a go at adding a unit test or two in the project. Your new role as the middleware test engineer will be looking for any and every opportunity
to use code to do automatic testing. I added a unittest for you to give you a flavour of how powerful they are. No human needed to  test everything
3. General code layout and conditional flow is something we'll pay attention to.

### Overall

It's a good start. We can see you can pull an app together and that you can think logically. The syntax, semantics and elegance will come over time. 



   
   


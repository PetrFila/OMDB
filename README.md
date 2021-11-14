# OMDB
Django search app challenge

This is a simple, single database table application for storing titles.
The application also uses the Open Movie Database API to look up the titles which are not available locally.

### IMPORTANT 
The original requirement is to include a search for an episode type as well. Playing around with the OMDB API, it didn't return any episode results and series type titles don't include any objects linking either to seasons or episodes.
I believe, the episode search type is there to implement local database table dependency for episodes being linked to the series.
However, this has not been implemented due to above-mentioned issue.
Another problem is that the OMDB API no longer provides multiple results, and it now always returns a single exact matched title.

### The search behaviour
* Clicking on the Search button without any keyword or title type returns all titles in the local database.
* Search by title type returns all titles of the selected type.

+ Searching with just a title name - searches in the OMDB database first. 
+ If title doesn't exist there, it searches in local database.
  + If title is in local database - display result
  + else redirect to home page and display error
+ If title exists in the OMDB, the data is pulled and compared to local database.
  + If the title is already available locally, the result is displayed and the data from OMDB is not stored.
  + If title is NOT already in the local database, the data is stored and displayed

* Search with title name and type - searches in the OMDB database first.
  * if the already exists, all titles containing the key word get displayed
  * if the title is NOT already in the local database, the data is stored and displayed
  

### How to run the app locally
* Clone the repository
> https://github.com/PetrFila/OMDB.git 
* Navigate to the project folder
> cd omdb

#### Installing virtual environment:
You can skip this part if you already have one installed on your machine.
* Pipenv has been used to run the app
virtual environment runs *pipenv*, version 2021.5.29
> brew install pipenv

* Run either your virtual environment or 
> pipenv shell
- this will start the virtual environment

#### Installing the requirements and running the app:
* Install all the packages necessary to run the app
> pip install -r requirements.txt

* Database is not included in this repository so please run the migration to create your own local one.
* The project is based on the build in SQLite3 db.
> python manage.py migrate

#### Adding OMDB API key otherwise the app will not work
* Create a new file *api_key.py* under the *search* folder and include there this JSON
> omdb = {
    'url': 'http://www.omdbapi.com/',
    'api_key': 'your API key goes here'
}
* You need to have your own API key to make it work

#### Running the actual application
> python manage.py runserver

### Testing
Available endpoints
* Home " / "
* Preview of found titles " /title "
* Title details page " /title/<title_id> "

#### The happy path
| Action | Result |
|--------|--------|
|click on Search|All locally stored titles should be displayed|
|select a type and click on Search|Only the specific type of titles - (movies or series) - should be returned|
|type a title name which is already in local database|all titles containing the search word should be returned|
|type a title name and select a type|all titles of that type containing the search word should be returned|
|type a title name which is not in the local database|it should display the result incl. a message saying the title has been searched on OMDB and saved to our local database|
|type a title name which is not in the local database, select a title type as well|it should display the result incl. a message saying the title has been searched on OMDB and saved to our local database|
|click on the image on each result|the detail page should appear with the title details|
|while on the detail page, change the ID - use another existing one|It should display the other title details|
|each page contains Home button|clicking on it should take the user to the home - search page|

#### The sad path - error handling
| Action | Result |
|--------|--------|
|while still on the detail page, change the ID - use a non existing integer|this should redirect the user to the home page and display an error message|
|while still on the detail page, change the ID - use a random string/character|this should display a Not found 404 page|
|refresh the app so you are back on the home page. Add *title* to the URL|this should redirect the user back to the home page and display an error message|
|use a wrong/misspelled title name - example *ong bag*|this should redirect the user back to the home page and display an error message|
|disconnect from the internet and search for a title which is not in the local database to trigger the OMDB call|this should redirect the user back to the home page and display an error message|
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from search.forms import SearchForm
from django.contrib import messages
from .models import Title
from django.forms.models import model_to_dict
from .http_call import get_title_from_OMDB
from django.views.generic import ListView, DetailView, FormView


class SearchView(FormView):
    model = Title
    template_name = 'search_form.html'
    form_class = SearchForm


class ResultView(ListView):
    template_name = 'display_results.html'

    def get(self, request, *args, **kwargs):

        # Return titles by type
        if request.GET['type'] != '' and request.GET['title'] == '':
            filtered_titles = filter_titles(request.GET['type'])
            return render(request, self.template_name, {'movies': filtered_titles[0], 'series': filtered_titles[1]})

        # Return all titles
        elif request.GET['title'] == '' and request.GET['type'] == '':
            titles = Title.objects.all()
            movies = titles.filter(type='movie')
            series = titles.filter(type='series')
            return render(request, self.template_name, {'movies': movies, 'series': series})

        # Search in OMDB and check local DB for existing title.
        else:
            omdb_result = get_title_from_OMDB(request)

            # Display error in case of problem with connection to OMDB
            if type(omdb_result) == str:  # I know this should have been handled better way but I'm, happy that it actually works.
                messages.error(request, omdb_result)
                return redirect('/')

            # Display error if title not found in OMDB nor locally
            elif omdb_result['Response'] == 'False':
                try:
                    Title.objects.get(title__exact=request.GET['title'])
                    filtered_titles = filter_titles(request.GET['title'])
                    return render(request, self.template_name, {'movies': filtered_titles[0], 'series': filtered_titles[1]})
                except ObjectDoesNotExist as er:
                    messages.error(request, er)
                    return redirect('/')

            # If the title already exists, don't save the OMDB result and display the local one
            # Else save the OMDB result and display it.
            elif omdb_result['Response'] == 'True':

                try:
                    exact_match = model_to_dict(Title.objects.get(title__exact=omdb_result['Title']))

                    if exact_match['type'] == omdb_result['Type'] and exact_match['title'] == omdb_result['Title'] and omdb_result['Type'] == 'movie':
                        filtered_titles = filter_titles(request.GET['title'])
                        return render(request, self.template_name, {'movies': filtered_titles[0]})

                    elif exact_match['type'] == omdb_result['Type'] and exact_match['title'] == omdb_result['Title'] and omdb_result['Type'] == 'series':
                        filtered_titles = filter_titles(request.GET['title'])
                        return render(request, self.template_name, {'series': filtered_titles[1]})

                    else:
                        add_new_title(omdb_result)
                        filtered_titles = filter_titles(request.GET['type'])
                        messages.success(request, 'Title found in the OMDB and has been added to the local database.')
                        return render(request, self.template_name, {'movies': filtered_titles[0], 'series': filtered_titles[1]})

                except ObjectDoesNotExist as er:
                    messages.error(request, er)
                    return redirect('/')

                except Exception as e:
                    print(e)
                    messages.error(request, e)
                    return redirect('/')


class DetailTitleView(DetailView):
    template_name = 'title_details.html'
    '''
    I'm not sure about adding the pk to the get method 
    but I couldn't find other way to check for the title in DB an eventually return an error. 
    Not using the get method works also fine but I couldn't find a way of handling the error for non existing title in DB
    other than getting Django generic 404 error page which is something I don't want.
    '''

    def get(self, request, pk, *args, **kwargs):
        # Try to get the title from DB
        try:
            title_details = Title.objects.get(pk=pk)
            return render(request, self.template_name, {'title': title_details})
        except ObjectDoesNotExist as er:
            # redirect here
            messages.error(request, er)
            return redirect('/')

# I tried to wrap this into a class view but it seemed to be just more complicated then this solution which works perfectly fine.
def add_new_title(omdb_result):
    add_to_db = Title(
        title=omdb_result['Title'],
        type=omdb_result['Type'],
        year=omdb_result['Year'],
        genre=omdb_result['Genre'],
        director=omdb_result['Director'],
        actor=omdb_result['Actors'],
        plot=omdb_result['Plot'],
        image_link=omdb_result['Poster'],
        IMDB_link='https://www.imdb.com/title/' + omdb_result['imdbID'] + '/'
    )
    add_to_db.save()


def filter_titles(filter_value):
    if filter_value == 'movie' or filter_value == 'series':
        titles = Title.objects.filter(type__contains=filter_value)
        movies = titles.filter(type='movie')
        series = titles.filter(type='series')
        return movies, series
    else:
        titles = Title.objects.filter(title__contains=filter_value)
        movies = titles.filter(type='movie')
        series = titles.filter(type='series')
        return movies, series

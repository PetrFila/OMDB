from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from search.forms import SearchForm
from django.contrib import messages
from .models import Title
from .http_call import get_title_from_OMDB
from django.views.generic import ListView, DetailView, FormView


class SearchView(FormView):
    model = Title
    template_name = 'search_form.html'
    form_class = SearchForm


class ResultView(ListView):
    template_name = 'display_results.html'

    def get(self, request, *args, **kwargs):
        if request.GET['type'] != '' and request.GET['title'] == '':
            titles = Title.objects.filter(type__contains=request.GET['type'])
            return render(request, self.template_name, {'titles': titles})

        elif request.GET['title'] == '' and request.GET['type'] == '':
            titles = Title.objects.all()
            return render(request, self.template_name, {'titles': titles})

        else:
            omdb_result = get_title_from_OMDB(request)

            if type(omdb_result) == str:  # I know this should have been handled better way but I'm, happy that it actually works.
                messages.error(request, omdb_result)
                return redirect('/')

            elif omdb_result['Response'] == 'False':
                messages.error(request, omdb_result['Error'])
                return redirect('/')

            elif omdb_result['Response'] == 'True':
                if Title.objects.filter(title__contains=request.GET['title']).exists():
                    titles = Title.objects.filter(title__contains=request.GET['title'])
                    return render(request, self.template_name, {'titles': titles})
                else:
                    add_new_title(omdb_result)
                    titles = Title.objects.filter(title__contains=request.GET['title'])
                    messages.success(request, 'Title found in the OMDB and has been added to the local database.')
                    return render(request, self.template_name, {'titles': titles})


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


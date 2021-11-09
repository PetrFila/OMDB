from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from search.forms import SearchForm
from django.contrib import messages
from .models import Title
from .http_call import get_title_from_OMDB
from django.views.generic import ListView, DetailView, CreateView, TemplateView


class SearchView(CreateView):
    model = Title
    template_name = 'search_form.html'
    form_class = SearchForm


class ResultView(ListView):
    template_name = 'display_results.html'

    def get(self, request, *args, **kwargs):
        # Render the search form again and display some extra friendly error message
        messages.error(request, 'Sorry. ' + request.method + ' method is not allowed.')
        return redirect('/')

    def post(self, request, *args, **kwargs):
        omdb_result = get_title_from_OMDB(request)
        if type(omdb_result) == str:  # I know this should have been handled better way but I'm, happy that it actually works.
            messages.error(request, omdb_result)
            return redirect('/')

        # titles_from_db = Title.objects.all()
        # return render(request, self.template_name, {'titles': titles_from_db})


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


def find_title(request):
    if request.method == 'POST' and request.POST['title'] != '' and request.POST['type'] != '':
        # if Title.objects.filter(title__contains=request.POST['title']).exists():
        #     titles = Title.objects.filter(title__contains=request.POST['title'])
        #     return render(request, 'display_results.html', {'titles': titles})
        # else:
        omdb_result = get_title_from_OMDB(request)
        if type(omdb_result) == str:  # I know this should have been handled better way but I'm, happy that it actually works.
            messages.error(request, 'Sorry mate. ' + omdb_result)
            return redirect('/')
        elif omdb_result['Response'] == 'True':
            add_new_title(omdb_result)
            messages.success(request, 'Title found in the OMDB and has been added to the local database.')
            titles = Title.objects.filter(title__contains=request.POST['title'])
            return render(request, 'display_results.html', {'titles': titles})
        elif omdb_result['Response'] == 'False':
            messages.error(request, 'Sorry mate. '+omdb_result['Error'])
            return redirect('/')

    elif request.method == 'POST' and request.POST['type'] != '':
        titles = Title.objects.filter(type__contains=request.POST['type'])
        return render(request, 'display_results.html', {'titles': titles})

    # elif request.method == 'POST' and request.POST['title'] == '' and request.POST['type'] == '':
    #     titles = Title.objects.order_by('title')
    #     return render(request, 'display_results.html', {'titles': titles})
    # else:
    #     # Render the search form again and display some extra friendly error message
    #     messages.error(request, 'Sorry mate. '+request.method+' method is not allowed.')
    #     return redirect('/')








def add_new_title(omdb_result):
    print(omdb_result)
    add_to_db = Title(
        title=omdb_result['Title'],
        type=omdb_result['Type'],
        year=omdb_result['Year'],
        genre=omdb_result['Genre'],
        director=omdb_result['Director'],
        actor=omdb_result['Actors'],
        plot=omdb_result['Plot'],
        image_link=omdb_result['Poster'],
        IMDB_link='https://www.imdb.com/title/'+omdb_result['imdbID']+'/'
    )
    add_to_db.save()


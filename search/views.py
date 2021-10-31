from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from search.forms import SearchForm
from django.contrib import messages
from .models import Title
from .http_call import get_title_from_OMDB
import time


def search_form(request):
    s_form = SearchForm
    return render(request, 'search_form.html', {'form': s_form})


def find_title(request):
    if request.method == 'POST' and request.POST['title'] != '':
        if Title.objects.filter(title__contains=request.POST['title']).exists():
            titles = Title.objects.filter(title__contains=request.POST['title'])
            return render(request, 'display_results.html', {'titles': titles})
        else:
            omdb_result = get_title_from_OMDB(request)
            if type(omdb_result) == str:  # I know thi should have been handled better way but I'm, happy that it actually works
                messages.error(request, 'Sorry mate. ' + omdb_result)
                return redirect('/')
            elif omdb_result['Response'] == 'False':
                messages.error(request, 'Sorry mate. '+omdb_result['Error'])
                return redirect('/')
            else:
                add_new_title(omdb_result)
                messages.success(omdb_result, 'Title found in the OMDB and has been added to the local database.')
                titles = Title.objects.filter(title=request.POST['title'])
                return render(request, 'display_results.html', {'titles': titles})

    elif request.method == 'POST' and request.POST['type'] != '':
        titles = Title.objects.filter(type__contains=request.POST['type'])
        return render(request, 'display_results.html', {'titles': titles})
    elif request.method == 'POST' and request.POST['title'] == '' and request.POST['type'] == '':
        titles = Title.objects.order_by('title')
        return render(request, 'display_results.html', {'titles': titles})
    else:
        # Render the search form again and display some extra friendly error message
        messages.error(request, 'Sorry mate. '+request.method+' method is not allowed.')
        return redirect('/')


def title_detail(request, pk):
    if Title.objects.filter(pk=pk).exists():
        title = Title.objects.get(pk=pk)
        return render(request, 'title_details.html', {'title': title})
    else:
        messages.error(request, 'Nah, sorry mate. There is no such a title in the database.')
        return redirect('/')





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


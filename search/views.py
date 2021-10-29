from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from search.forms import SearchForm
from django.contrib import messages
from .models import Title
import requests
import time
# from rest_framework import status
# from rest_framework.response import Response

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
            add_new_title(omdb_result)
            titles = Title.objects.filter(title__contains=request.POST['title'])
            return render(request, 'display_results.html', {'titles': titles})



    elif request.method == 'POST' and request.POST['type'] != '':
        titles = Title.objects.filter(type__contains=request.POST['type'])
        return render(request, 'display_results.html', {'titles': titles})
    elif request.method == 'POST' and request.POST['title'] == '' and request.POST['type'] == '':
        titles = Title.objects.order_by('title')
        return render(request, 'display_results.html', {'titles': titles})
    else:
        # Render the search form again and display some extra friendly error message
        messages.error(request, 'Sorry mate. No search request has been made.')
        return redirect('/')


def title_detail(request, pk):
    if Title.objects.filter(pk=pk).exists():
        title = Title.objects.get(pk=pk)
        return render(request, 'title_details.html', {'title': title})
    else:
        messages.error(request, 'Nah, sorry mate. There is no such a title in the database.')
        return redirect('/')


def get_title_from_OMDB(request):
    if request.method == "POST":
        attempt_num = 0  # keep track of how many times we've retried
        while attempt_num < 3:
            url = 'http://www.omdbapi.com/'
            payload = {'apikey': '2f18a196',
                       't': request.POST['title'],
                       'type': request.POST['type'],
                       'plot': 'full'}
            r = requests.get(url, params=payload)
            if r.status_code == 200:
                attempt_num = 3
                data = r.json()
                return data
        #     else:
        #         attempt_num += 1
        #         # You can probably use a logger to log the error here
        #         time.sleep(5)  # Wait for 5 seconds before re-trying
        # return Response({"error": "Request failed"}, status=r.status_code)
    # else:
    #     return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)

def add_new_title(omdb_result):
    print(omdb_result)
    # Title.objects.create(
    #     title=omdb_result['Title'],
    #     type = omdb_result['type'],
    #     year = omdb_result['Title'],
    #     genre = omdb_result['Genre'],
    #     director = omdb_result['Director'],
    #     actor = omdb_result['Actors'],
    #     plot = omdb_result['Director'],
    #     image_link = omdb_result['Poster'],
    #     IMDB_link=omdb_result['IMDB_link']
    # )

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
        # post = form.save(commit=False)
    # post.author = request.user
    # post.published_date = timezone.now()
    # post.save()
    # return redirect('post_detail', pk=post.pk)

    # return render(request, 'blog/post_edit.html', {'form': form})

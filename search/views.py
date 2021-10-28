from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from search.forms import SearchForm
from django.contrib import messages
from .models import Title


def search_form(request):
    s_form = SearchForm
    return render(request, 'search_form.html', {'form': s_form})


def find_title(request):
    if request.method == 'POST' and request.POST['title'] != '':
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
        messages.error(request, 'Nah, sorry mate. There is no such title in the database.')
        return redirect('/')

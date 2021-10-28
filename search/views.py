from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from search.forms import SearchForm
from django.contrib import messages
from .models import Title


def search_form(request):
    s_form = SearchForm
    return render(request, 'search_form.html', {'form': s_form})


def find_title(request):
    if request.method == 'POST' and request.POST['title'] is not '':
        titles = Title.objects.filter(title__contains=request.POST['title'])
        return render(request, 'display_results.html', {'titles': titles})
    elif request.method == 'POST' and request.POST['type'] is not '':
        titles = Title.objects.filter(type__contains=request.POST['type'])
        return render(request, 'display_results.html', {'titles': titles})
    elif request.method == 'POST' and request.POST['title'] is '' and request.POST['type'] is '':
        titles = Title.objects.order_by('title')
        return render(request, 'display_results.html', {'titles': titles})
    else:
        # Render the search form again and display some extra friendly error message
        messages.error(request, 'Sorry mate. No search request has been made.')
        return redirect('/')


def title_detail(request, pk):
    title = get_object_or_404(Title, pk=pk)
    return render(request, 'title_details.html', {'title': title})

from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from search.forms import SearchForm


def search_form(request):
    s_form = SearchForm
    return render(request, 'search_form.html', {'form': s_form})


def find_title(request):
    # return HttpResponse('This is the title you have searched for')
    # titles = Title.objects.get()
    return render(request, 'display_results.html')

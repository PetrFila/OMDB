from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from search.forms import SearchForm
from django.contrib import messages



def search_form(request):
    print(request)
    s_form = SearchForm
    return render(request, 'search_form.html', {'form': s_form})


def find_title(request):
    if request.method == 'POST':
        print(request)

        # titles = Title.objects.get()
        return render(request, 'display_results.html')
    else:
        # Render the search form again and display some extra friendly error message
        print('Not POST method')
        messages.error(request, 'Sorry mate. No search request has been made.')

        return redirect('/')

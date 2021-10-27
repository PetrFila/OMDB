from django.contrib import admin
from .models import Title


class SearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'year', 'genre', 'director', 'actor', 'plot', 'IMDB_link')


admin.site.register(Title, SearchAdmin)








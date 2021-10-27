from django import forms
from .models import Title


class SearchForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ('title', 'type')


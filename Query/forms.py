import os

from django import forms
from django.core.exceptions import ValidationError
from Query.choices import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class GenreForm(forms.Form):
    genre = forms.ChoiceField(choices=GENRE_CHOICES, label="", initial='', widget=forms.Select())


    def clean_genre(self):
        data = self.cleaned_data['genre']

        genre_file = os.path.join(BASE_DIR, "Query/data/genre.txt")
        genre_set = set()

        with open(genre_file) as fp:
            line = fp.readline()
            while line:
                genre_set.add(line[:-1])
                line = fp.readline()
        
        if data not in genre_set:
            raise ValidationError(('Invalid genre'))
        
        return data

class PlatForm(forms.Form):
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES, label="", initial='', widget=forms.Select())

    def clean_plat(self):
        data = self.cleaned_data['platform']

        plat_file = os.path.join(BASE_DIR, "Query/data/platform.txt")
        plat_set = set()

        with open(plat_file) as fp:
            line = fp.readline()
            while line:
                plat_set.add(line[:-1])
                line = fp.readline()
        
        if data not in plat_set:
            raise ValidationError(('Invalid genre'))
        
        return data
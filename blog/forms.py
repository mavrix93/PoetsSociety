from django import forms

from .models import Poem


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = ('poet','title', 'text','poets_group', 'visibility')

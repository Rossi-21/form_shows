from django import forms
from django.forms import ModelForm
from .models import Show

class CreateShowForm(forms.ModelForm):
    class Meta:

        model = Show

        fields = ('title', 'network', 'release_date', 'description')

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control'}),
            'network' : forms.TextInput(attrs={'class' : 'form-control'}),
            'release_date' : forms.DateInput(attrs={'type' :'date', 'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'})
        }


from django import forms
from django.forms import ModelForm
from .models import Show
from django.utils import timezone


class CreateShowForm(forms.ModelForm):
    class Meta:

        model = Show

        fields = ('title', 'network', 'release_date', 'description')

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control mb-2'}),
            'network' : forms.TextInput(attrs={'class' : 'form-control mb-2'}),
            'release_date' : forms.DateInput(attrs={'type' :'date', 'class' : 'form-control mb-2'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super(CreateShowForm, self).clean()

        title = self.cleaned_data.get('title')
        network = self.cleaned_data.get('network')
        release_date = self.cleaned_data.get('release_date')
        description = self.cleaned_data.get('description')

        if len(title) < 3:
            self._errors['title'] = self.error_class([
                'Title must be at least 3 Characters'
            ])
        if len(network) < 2:
            self._errors['network'] = self.error_class([
                'Network must be at least 2 characters'
            ])
        if release_date and release_date > timezone.now().date():
            self._errors['release_date'] = self.error_class([
                'Release date cannot be in the future'
            ])
        if len(description) < 8:
            self._errors['description'] = self.error_class([
                'Description must be at least 8 characters'
            ])

        return cleaned_data



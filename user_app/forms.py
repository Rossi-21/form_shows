from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_image',)
        
        profile_image = forms.ImageField(label = "Profile Picture")


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class' : 'form-control',
            })
        self.fields['email'].widget.attrs.update({
            'class' : 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'class' : 'form-control',
            })
        self.fields['password2'].widget.attrs.update({
            'class' : 'form-control',
            })
    class Meta:

        model = User

        fields = ['username', 'email', 'password1', 'password2']
class CreateShowForm(forms.ModelForm):
    class Meta:

        model = Show

        fields = ('title', 'network', 'release_date', 'description', 'show_image')

        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control mb-2'}),
            'network' : forms.TextInput(attrs={'class' : 'form-control mb-2'}),
            'release_date' : forms.DateInput(attrs={'type' :'date', 'class' : 'form-control mb-2'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(CreateShowForm, self).clean()

        title = self.cleaned_data.get('title')
        network = self.cleaned_data.get('network')
        release_date = self.cleaned_data.get('release_date')
        description = self.cleaned_data.get('description')

        if title and len(title) < 3:
            self._errors['title'] = self.error_class([
                'Title must be at least 3 Characters'
            ])
        if network and len(network) < 2:
            self._errors['network'] = self.error_class([
                'Network must be at least 2 characters'
            ])
        if release_date and release_date > timezone.now().date():
            self._errors['release_date'] = self.error_class([
                'Release date cannot be in the future'
            ])
        if description and len(description) < 8:
            self._errors['description'] = self.error_class([
                'Description must be at least 8 characters'
            ])

        return cleaned_data



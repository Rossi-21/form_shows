from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import os

from .models import *

# Upload and Update Image Form
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label = "Profile Picture")
    class Meta:
        model = Profile
        fields = ('profile_image',)

    # Image Form Validation    
    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        # If the form is submitted
        if profile_image:
            # Create a variable that splits the imagename and puts the filetype in lowercase
            ext = os.path.splitext(profile_image.name)[1].lower()
            # If the name does not contain .jpg, .jpeg, .png throw a validtion error
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError('Only JPEG or PNG files are allowed.')

        return profile_image

# Create User Form
class CreateUserForm(UserCreationForm):
    # Method Allowing Bootstrap CSS & other CSS classes 
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
        # Which fields will appear in the form
        fields = ['username', 'email', 'password1', 'password2']

# Create Show Form
class CreateShowForm(forms.ModelForm):
    class Meta:
        model = Show
        # Which fields will apear in the form
        fields = ('title', 'network', 'release_date', 'description', 'show_image')
        # Useing widget functionality to allow Bootstrap & other CSS classes
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'form-control mb-2'}),
            'network' : forms.TextInput(attrs={'class' : 'form-control mb-2'}),
            'release_date' : forms.DateInput(attrs={'type' :'date', 'class' : 'form-control mb-2'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
        }
    # Show Image Upload Validation
    def clean_show_image(self):
        show_image = self.cleaned_data.get('show_image')

        if show_image:
             # Create a variable that splits the imagename and puts the filetype in lowercase
            ext = os.path.splitext(show_image.name)[1].lower()
            # If the name does not contain .jpg, .jpeg, .png throw a validtion error
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError('Only JPEG or PNG files are allowed.')

        return show_image

    # Create Show Form Validation
    def clean(self):
        # Create a variable for the validation method
        cleaned_data = super(CreateShowForm, self).clean()
        # Create variables for each of the form fields
        title = self.cleaned_data.get('title')
        network = self.cleaned_data.get('network')
        release_date = self.cleaned_data.get('release_date')
        description = self.cleaned_data.get('description')
        # Specific Validation for each of the form fields
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



from django.shortcuts import render, redirect
from .models import *
from .forms import CreateShowForm

def home(request):

    form = CreateShowForm()

    if request.method == 'POST':

        form = CreateShowForm(request.POST)

        if form.is_valid():
            
            form.save()

            return redirect('allShows')
        
    context = {
        'form' : form,
    }

    return render(request, "index.html", context)

def allShows(request):
    shows = Show.objects.all()

    context = {
        'shows' : shows,
    }
    return render(request, "shows.html", context )

# Create your views here.

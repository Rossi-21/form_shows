from django.shortcuts import render, redirect
from .models import *
from .forms import *

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

def viewShow(request, id):

    show = Show.objects.get(id=id)
    
    context = {
        'show' : show
    }
    return render(request, 'view.html', context)

def allShows(request):

    shows = Show.objects.all()

    context = {
        'shows' : shows,
    }
    return render(request, "shows.html", context )

def editShow(reqeust, id):

    show = Show.objects.get(id=id)
    
    form = UpdateShowForm

    context ={
        'show' : show,
        'form' : form
    }

    return render(reqeust, 'edit.html', context)

def updateShow(request, id):

    show = Show.objects.get(id=id)

    form = UpdateShowForm()

    if request.method == 'POST':

        form = UpdateShowForm(request.POST)

        if form.is_valid:

            form.save()

        return redirect(f'/shows/{show.id}', show)
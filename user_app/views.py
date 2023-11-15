from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
from .forms import *

def registerUser(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('allShows')
    
    context = {
        'form' : form
    }

    return render(request, 'register.html', context)

def loginUser(request):
    
    if request.method  == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:

            login(request, user)

            return redirect('allShows')
        
        else:

            messages.info(request, 'Username or Password is incorrect')       

    context = {}

    return render(request, 'login.html', context)

def logoutUser(request):

    logout(request)

    return redirect('loginUser')

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

def editShow(request, id):

    show = Show.objects.get(id=id)

    form = CreateShowForm(instance=show)

    if request.method == 'POST':

        form = CreateShowForm(request.POST, instance=show)

        if form.is_valid():

            form.save()

        return redirect(f'/shows/{show.id}', show)

    context ={
        'show' : show,
        'form' : form
    }

    return render(request, 'edit.html', context)

def deleteShow(reqeust, id):
    
    show = Show.objects.get(id=id)

    show.delete()
    
    return redirect('allShows')

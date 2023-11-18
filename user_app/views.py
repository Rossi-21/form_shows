from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def showUser(request, id):

    user = User.objects.get(id=id)

    shows = Show.objects.filter(user=user)

    context = {
        'user' : user,
        'shows' : shows
    }

    return render(request, "user.html", context)

def logoutUser(request):

    logout(request)

    return redirect('loginUser')

@login_required
def home(request):

    form = CreateShowForm()

    if request.method == 'POST':

        form = CreateShowForm(request.POST)

        if form.is_valid():
            show = form.save(commit=False)
            show.user = request.user
            form.save()

            return redirect('allShows')
        
    context = {
        'form' : form,
    }

    return render(request, "index.html", context)

@login_required
def viewShow(request, id):

    show = Show.objects.get(id=id)
    
    context = {
        'show' : show
    }
    return render(request, 'view.html', context)

@login_required      
def allShows(request):

    user = request.user
    shows = Show.objects.all()

    context = {
        'user' : user,
        'shows' : shows,
    }

    return render(request, "shows.html", context )

@login_required
def likeShow(reqeust, id):
    show = Show.objects.get(id=id)

    show.like.add(reqeust.user)

    return redirect('allShows')

@login_required
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

@login_required
def deleteShow(reqeust, id):
    
    show = Show.objects.get(id=id)

    show.delete()
    
    return redirect('allShows')

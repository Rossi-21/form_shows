from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
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

    return render(request, 'login.html')

@login_required
def showUser(request, id):

    user = User.objects.get(id=id)
    profile = Profile.objects.get(id=request.user.id)
    shows = Show.objects.filter(user=user)
    favorites = Show.objects.filter(like=user)

    context = {
        'user' : user,
        'profile' :profile,
        'shows' : shows,
        'favorites' : favorites
    }

    return render(request, "user.html", context)

@login_required
def updateUser(request, id):

    user = User.objects.get(id=id)
    profile = Profile.objects.get(user__id=id)

    user_form = CreateUserForm(instance=user)
    profile_form = ProfilePicForm(instance=profile)

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST or None, request.FILES or None, instance=user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            login(request, user)

            return redirect(f'/user/{user.id}')
        
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'profile' : profile
    }

    return render(request, "updateUser.html", context)

def updateImage(request, id):

    user = User.objects.get(id=id)
    profile = Profile.objects.get(user__id=id)

    form = ProfilePicForm(instance=profile)

    if request.method == 'POST':
        form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile)

        if form.is_valid():
            form.save()

            return redirect(f'/user/{user.id}')

    context = {
        'profile' : profile,
        'form' : form,
    }

    return render(request, "updateImage.html", context)

def logoutUser(request):

    logout(request)

    return redirect('loginUser')

@login_required
def home(request):

    profile = Profile.objects.get(user__id=request.user.id)

    form = CreateShowForm()

    if request.method == 'POST':
        form = CreateShowForm(request.POST, request.FILES)

        if form.is_valid():
            show = form.save(commit=False)
            show.user = request.user
            form.save()

            return redirect('allShows')
        
    context = {
        'form' : form,
        'profile':profile
    }

    return render(request, "index.html", context)

@login_required
def viewShow(request, id):

    profile = Profile.objects.get(user__id=request.user.id)
    show = Show.objects.get(id=id)
    comments = show.comment.all()

    if request.method == 'POST':
        user = request.user
        show = Show.objects.get(id=id)
        description = request.POST.get('description')

        new_comment = Comment.objects.create(description = description, user = user)
        show.comment.add(new_comment)

        return redirect(f'/shows/{show.id}')

    context = {
        'show' : show,
        'comments' : comments,
        'profile' :profile
    }

    return render(request, 'view.html', context)

@login_required      
def allShows(request):

    user = request.user
    profile = Profile.objects.get(user__id=user.id)
    shows = Show.objects.all()
    favorites = Show.objects.filter(like=user)

    context = {
        'user' : user,
        'shows' : shows,
        'favorites' : favorites,
        'profile' : profile
    }
    
    return render(request, "shows.html", context )

@login_required
def likeShow(request, id):
    
    if request.method =="POST":
        show = Show.objects.get(id=id)

        if request.user not in show.like.all():
            show.like.add(request.user)
        else:
            show.like.remove(request.user)

    return redirect('allShows')

@login_required
def editShow(request, id):

    profile = Profile.objects.get(user__id=request.user.id)
    show = Show.objects.get(id=id)

    form = CreateShowForm(instance=show)

    if request.method == 'POST':
        form = CreateShowForm(request.POST or None, request.FILES or None, instance=show)

        if form.is_valid():
            form.save()

        return redirect(f'/shows/{show.id}', show)

    context ={
        'show' : show,
        'form' : form,
        'profile' : profile
    }

    return render(request, 'edit.html', context)

@login_required
def deleteShow(reqeust, id):
    
    show = Show.objects.get(id=id)

    show.delete()
    
    return redirect('allShows')

@login_required
def deleteComment(request, id):

    comment = Comment.objects.get(id=id)

    comment.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))
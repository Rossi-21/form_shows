from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
#email imports
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import requests

from .models import *
from .forms import *

api_key = settings.API_KEY
email_password = settings.EMAIL_HOST_PASSWORD
email_address = settings.EMAIL_ADDRESS

# Register user function
def registerUser(request):
    # Display the user creation form
    form = CreateUserForm()

    if request.method == 'POST':
        # Grab the submitted info from the form
        form = CreateUserForm(request.POST)

        if form.is_valid():
            # Save the user & log them in
            user = form.save()
            login(request, user)
            # Send the new user and email
            subject = 'Welcome to the TV Party!'
            html_message = render_to_string('registration_email.html', {'user': user})
            plain_message = strip_tags(html_message)
            from_email = 'email_address'
            to = [user.email]

            send_mail(subject, plain_message, from_email, to, html_message=html_message )

            #Rredirect them to the dashboard
            return redirect('allShows')
    
    context = {
        'form' : form
    }

    return render(request, 'register.html', context)

# Login user function
def loginUser(request):

    if request.method  == "POST":
        # Get the username and password from the database
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Verify the username and password
        user = authenticate(request, username = username, password = password)

        if user is not None:
            # If the user exists log them in
            login(request, user)
            # Redirect to the dashboard
            return redirect('allShows')
        
        else:
            # If the user does not exist, display an error message
            messages.info(request, 'Username or Password is incorrect')       

    return render(request, 'login.html')

# Display user info page
@login_required
def showUser(request, id):
    # Get the user & the profile,shows and favorites associated with the user
    user = User.objects.get(id=id)
    profile = Profile.objects.get(id=request.user.id)
    shows = Show.objects.filter(user=user)
    favorites = Show.objects.filter(like=user)

    # Allow other users to follow our unfollow the user displayed on the page
    if request.method == "POST":
        # Create a veriable for the Logged In user
        current_user_profile = request.user.profile
        # Create a veriable for the form action
        action = request.POST['follow']
        # If unfollow, remove the viewed user from the Logged In users follows list
        if action == "unfollow":
            current_user_profile.follows.remove(user.id)
        # If follow, add the viewed user to the Logged In users follows list
        elif action == "follow":
            current_user_profile.follows.add(user.id)
        # Save the Logged in users profile
        current_user_profile.save()

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

    user_form = CreateUserForm(instance=user)

    if request.method == 'POST':
        user_form = CreateUserForm(request.POST or None, instance=user)

        if user_form.is_valid():
            user_form.save()
            
            login(request, user)

            return redirect(f'/user/{user.id}')
        
    context = {
        'user_form' : user_form,
    }

    return render(request, "updateUser.html", context)

@login_required
def deleteUser(request, id):
    user = User.objects.get(id=id)
    user.delete()

    return redirect("registerUser")

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
    shows = Show.objects.all().order_by('-created_at')
    favorites = Show.objects.filter(like=user)

    URL = "https://api.openai.com/v1/chat/completions"

    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f"What is the first TV show in the world?"}],
    "temperature" : 1.0,
    "top_p":1.0,
    "n" : 1,
    "stream": False,
    "presence_penalty":0,
    "frequency_penalty":0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)
    data = response.json()
   
    context = {
        'user' : user,
        'shows' : shows,
        'favorites' : favorites,
        'profile' : profile,
        'data' : data
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
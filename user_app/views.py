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
email_address = settings.EMAIL_HOST_USER

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
            return redirect('dashboard')
    
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
            return redirect('dashboard')
        
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

    return render(request, "showUser.html", context)

# Update User Method
@login_required
def updateUser(request, id):
    # Get the User by id
    user = User.objects.get(id=id)
    # Grab the Create User Form from forms.py for the view with the info currently in the database
    user_form = CreateUserForm(instance=user)

    if request.method == 'POST':
        # Process the Create User Form
        user_form = CreateUserForm(request.POST or None, instance=user)

        if user_form.is_valid():
            # Save the edited form to the database
            user_form.save()
            # Login the user
            login(request, user)
            # return to the View User page
            return redirect(f'/user/{user.id}')
        
    context = {
        'user_form' : user_form,
    }

    return render(request, "updateUser.html", context)

# Delete User Method
@login_required
def deleteUser(request, id):
    # Get the User by id
    user = User.objects.get(id=id)
    # Delete the User object form the database
    user.delete()
    # Send the User back to the registration page
    return redirect("registerUser")

# Update the User Image Method
@login_required
def updateImage(request, id):
    # Get the User by id
    user = User.objects.get(id=id)
    # Get the Profile associated with that User
    profile = Profile.objects.get(user__id=id)
    # Get the Profile Picture Form from forms.py
    form = ProfilePicForm(instance=profile)

    if request.method == 'POST':
        # Process the Profile Picture Form
        form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile)

        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Send the User back to the View User page
            return redirect(f'/user/{user.id}')

    context = {
        'profile' : profile,
        'form' : form,
    }

    return render(request, "updateImage.html", context)

# Logout User Method
@login_required
def logoutUser(request):
    # Logout the User
    logout(request)
    # Send the User back to the Login page
    return redirect('loginUser')

# Create Show Method
@login_required
def createShow(request):
    # Dispaly the User Profile Image
    profile = Profile.objects.get(user__id=request.user.id)
    # Display the Create Show Form from forms.py
    form = CreateShowForm()

    if request.method == 'POST':
        # Process the Create Show Form
        form = CreateShowForm(request.POST, request.FILES)

        if form.is_valid():
            # Get the show instance without saving it to the database
            show = form.save(commit=False)
            # Associate the current User with the show being created
            show.user = request.user
            # Save the new show instance to the database
            form.save()
            # Send the User to the dashbaord
            return redirect('dashboard')
        
    context = {
        'form' : form,
        'profile':profile
    }

    return render(request, "createShow.html", context)

# View a Show Method
@login_required
def showShow(request, id):
    # Dispaly the User Profile Image
    profile = Profile.objects.get(user__id=request.user.id)
    # Get the Show by id
    show = Show.objects.get(id=id)
    # Get all of the comments related to that show
    comments = show.comment.all()

    if request.method == 'POST':
        # Get the current User
        user = request.user
        # Get the Show by id
        show = Show.objects.get(id=id)
        # Process the comment form
        description = request.POST.get('description')
        # Create a Comment object with the description from the form and associate it with the current User
        new_comment = Comment.objects.create(description = description, user = user)
        # Save the comment to the database
        show.comment.add(new_comment)
        # Keep the User on the same page so they can view thier Comment
        return redirect(f'/shows/{show.id}')

    context = {
        'show' : show,
        'comments' : comments,
        'profile' :profile
    }

    return render(request, 'showShow.html', context)

# Dashboard Method
@login_required      
def dashboard(request):
    # Get the current User
    user = request.user
    # Display the User Profile image
    profile = Profile.objects.get(user__id=user.id)
    # Get all the shows in order of the create_at date
    shows = Show.objects.all().order_by('-created_at')
    # Allow Users to Like Shows
    favorites = Show.objects.filter(like=user)

    # Connect to ChatGPT API
    URL = "https://api.openai.com/v1/chat/completions"
    # ChatGPT Configuration
    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{
        "role": "user", 
        # ChatGPT Prompt
        "content": f"""You are an expert on the History of Television. 
                    You have a deep understading of all things related to Television.
                    Give a random fact from Television History.
                    """
        }],
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
    # Get the response from the ChatGPT API
    response = requests.post(URL, headers=headers, json=payload, stream=False)
    # Save the json response as a veriable called data
    data = response.json()
   
    context = {
        'user' : user,
        'shows' : shows,
        'favorites' : favorites,
        'profile' : profile,
        'data' : data
    }
    
    return render(request, "dashboard.html", context )

# Like shows method
@login_required
def likeShow(request, id):
    
    if request.method =="POST":
        # Get the show by id
        show = Show.objects.get(id=id)
        # If the User does not Like the show allow them to Like it
        if request.user not in show.like.all():
            # Add the Users Like to the database
            show.like.add(request.user)
        # If the User dose Like the Show allow them to unLike it
        else:
            # Delete the Users Like from the database
            show.like.remove(request.user)
    # Send the User to the Dashboard page
    return redirect('dashboard')

# Update Show Method
@login_required
def updateShow(request, id):
    # Dispaly the User Profile Image
    profile = Profile.objects.get(user__id=request.user.id)
    # Get the Show by id
    show = Show.objects.get(id=id)
    # Display the Create Show Form with the current information from the database
    form = CreateShowForm(instance=show)

    if request.method == 'POST':
        # Process the Create Show Form 
        form = CreateShowForm(request.POST or None, request.FILES or None, instance=show)

        if form.is_valid():
            # Save the upadate Show object to the database
            form.save()
        
        #Send the User to the Shows page
        return redirect(f'/shows/{show.id}', show)

    context ={
        'show' : show,
        'form' : form,
        'profile' : profile
    }

    return render(request, 'updateShow.html', context)

# Delete Show Method
@login_required
def deleteShow(reqeust, id):
    # Get the Show by id
    show = Show.objects.get(id=id)
    # Remove the Show from the database
    show.delete()
    # Send the User to the Dashboard 
    return redirect('dashboard')

# Delete Comment Method
@login_required
def deleteComment(request, id):
    # Get the Comment by id
    comment = Comment.objects.get(id=id)
    # Remove the Comment from the Database
    comment.delete()
    # Keep the User on the page
    return redirect(request.META.get('HTTP_REFERER', '/'))
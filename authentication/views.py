from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import UserProfile

@login_required
def edit_profile(request):
    try:
        form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
    except User.userprofile.RelatedObjectDoesNotExist:
        # Create a new profile for the user if it doesn't exist
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)  # Avoid saving twice
            user_profile.user = request.user
            user_profile.save()  # Now save the profile with the user association
            
            return redirect('dashboard')

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'authentication/edit_profile.html', {'form': form})

@login_required
def view_profile(request):
    try:
        user_profile = request.user.userprofile
        if not user_profile.profile_pic:
            # If not, use the default profile picture
            user_profile.profile_pic = 'default_profile_pic/default.jpg'
    except UserProfile.DoesNotExist:
        # Handle the case where the user doesn't have a profile yet (optional)
        messages.info(request, 'You haven\'t created a profile yet.')
        return redirect('create_profile')  # Redirect to profile creation view if desired
    
    return render(request, 'authentication/view_profile.html', {'user_profile': user_profile})


from tasks.models import Project
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
    
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Account created successfully!")
        return redirect('home')  # Redirect to sign-in page after successful sign-up


    return render(request, "authentication/index.html")

def signin(request):

    if request.method=="POST":
        username = request.POST["login-username"]
        pass1 = request.POST["login-pass1"]

        user=authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            return redirect('dashboard')

        else:
            messages.error(request,"  Wrong Username or Password  ")
            return redirect('home')
    return render(request, "authentication/index.html")

def signout(request):
    logout(request)
    
    
    return redirect("home")

@login_required
def dashboard(request):
    fname = request.user.first_name
    user_created_projects = Project.objects.filter(created_by=request.user)
    user_collaborating_projects = Project.objects.filter(collaborators=request.user)
    user_id = request.user.id
    return render(request, 'authentication/dashboard.html', {'user_projects': user_created_projects,'fname': fname, 'user_id': user_id,'user_collaborating_projects': user_collaborating_projects})

def contact(request):
    if request.method=='POST':
        message_name=request.POST['Reset Password']
        message_email=request.POST['message-email']
        message_name=request.POST['Hi use this code to reset password']
       
        # send_mail(message-name,
        # message,
        # settings.EMAIL_HOST_USER ,
        # [profile.mail],
        # )



def back_to_dashboard(request):
    return redirect('dashboard')

def search_by_username(request):
    project_id = request.GET.get('project_id')  # Get the project_id from the request

    if 'username' in request.GET:
        username = request.GET['username']
        users = User.objects.filter(username__icontains=username)
    else:
        users = User.objects.none()  # Return an empty queryset if no username provided

    return render(request, 'search_results.html', {'users': users, 'project_id': project_id})

def view_profile_from_search(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'authentication/view_profile.html', {'user_profile': user_profile})


from django.contrib.auth.forms import PasswordResetForm

# In your view function
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            # Redirect or show success message
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})
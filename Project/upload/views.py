from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.core.exceptions import ObjectDoesNotExist
from .models import MediaFile, Profile
from .decorators import unauthenticated_user, allowed_users

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        Profile.objects.create(user=request.user)
        profile = request.user.profile
        
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        print(request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)

@unauthenticated_user
def login_process(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                profile = user.profile
            except ObjectDoesNotExist:
                Profile.objects.create(user=user)

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'login.html')

@login_required(login_url='loginPage')
def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # Save file to media directory
        media_file = MediaFile.objects.create(user=request.user, file=file)
        messages.success(request, 'File uploaded successfully')
        return redirect('home')

    media_files = MediaFile.objects.filter(user=request.user)
    context = {'user': request.user, 'media_files': media_files}
    return render(request, 'home.html', context)

def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account is successfully created for ' + user)
            return redirect('loginPage')
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def logoutuser(request):
    logout(request)
    return redirect('loginPage')

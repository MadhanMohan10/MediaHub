from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from .models import MediaFile
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def login_process(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
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

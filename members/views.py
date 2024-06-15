from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import RegisterUserForm, EditUserForm
from django.contrib.auth.models import User


def update_password(request, user_id):
    user = User.objects.get(pk=user_id)
    form = PasswordChangeForm(user, request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, ("Password updated"))
        return redirect('login')

    return render(request,
        'authenticate/update_password.html', {
        'user': user,
        'form': form,
        })

def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    initial = {'image': user.profilepic.image}
    form = EditUserForm(request.POST or None, request.FILES or None, instance=user, initial = initial)
    if form.is_valid():
        form.save()
        messages.success(request, ("User updated"))
        return redirect('home')

    return render(request,
        'authenticate/update_user.html', {
        'user': user,
        'form': form,
        })


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("registration done"))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })

def logout_user(request):
    logout(request)
    messages.success(request, ("logged out"))
    return render(request, 'events/home.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request,("error logging in"))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})






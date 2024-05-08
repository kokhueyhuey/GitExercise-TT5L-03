from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout

from django.contrib import messages
from django import forms
from .forms import CreateUserForm, UserUpdateForm, OwnerUpdateForm, PetForm

# Create your views here.

def BookingPage(request):

    context = {}
    return render(request, 'bookingpage.html', context)

def PetprofilePage(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'account has been updated')
            return redirect('petprofile')
    else:
        form = PetForm()

    context = {'form':form}
    return render(request, 'petprofile.html', context)


def profilePage(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        o_form = OwnerUpdateForm(request.POST, request.FILES, instance=request.user.owner)
        if u_form.is_valid() and o_form.is_valid():
            u_form.save()
            o_form.save()
            messages.success(request, f'account has been updated')
            return redirect('profile')
    else: 
        u_form = UserUpdateForm(instance=request.user)
        o_form = OwnerUpdateForm(instance=request.user.owner)
    

    context = {
        'u_form' : u_form,
        'o_form' : o_form,
    }
    
    return render(request, 'profile.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')

                messages.success(request,'Account was successfully created!')

                return redirect('login')

        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)    
    return redirect('home')

def home(request):
    context={}
    return render(request, "home.html", context)
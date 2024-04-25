from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .forms import CreateUserForm

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form':form}
    return render(request, 'register.html', context)

def loginPage(request):
    form = UserCreationForm()
    context = {'form':form}
    return render(request, 'login.html', context)

def home(request):
    context={}
    return render(request, "home.html", context)




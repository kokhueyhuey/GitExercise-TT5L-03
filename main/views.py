from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout

from django.contrib import messages
from django import forms
from .forms import CreateUserForm, UserUpdateForm, OwnerUpdateForm, PetForm, BookingForm
from .models import Pet, Owner, Booking
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_only
from django.contrib.auth.models import Group

@admin_only
def AdminPage(request):
    sort_by = request.GET.get('sort_by', 'date')

    if sort_by == 'date':
        ongoing_bookings = Booking.objects.filter(status='Ongoing').order_by('-date')
        completed_bookings = Booking.objects.filter(status='Completed').order_by('-date')
        cancelled_bookings = Booking.objects.filter(status='Cancelled').order_by('-date')
    elif sort_by == 'id':
        ongoing_bookings = Booking.objects.filter(status='Ongoing').order_by('id')
        completed_bookings = Booking.objects.filter(status='Completed').order_by('id')
        cancelled_bookings = Booking.objects.filter(status='Cancelled').order_by('id')
  
    owners = Owner.objects.all()
    context = {'ongoing_bookings': ongoing_bookings, 
               'completed_bookings': completed_bookings,  
               'cancelled_bookings': cancelled_bookings,
               'owners': owners,
              }
    return render(request, 'admin_dashboard.html', context)


def BookingPage(request):
    if request.method == 'POST':
        form = BookingForm(request.user.owner, request.POST)
        print(form.errors)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user.owner
            booking.save()
            messages.success(request, f'booking has been updated')
            return redirect('bookingpage')
    else:
        form = BookingForm(request.user.owner)

    context = {'form': form }
    return render(request, 'bookingpage.html', context)

def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    owner = booking.owner  # Retrieve the owner associated with the booking
    if request.method == 'POST':
        form = BookingForm(owner, request.POST, instance=booking)
        print(form.errors)
        if form.is_valid():
            form.save()  
            return redirect('admin_dashboard')  
    else:
        form = BookingForm(owner, instance=booking)  
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})


def change_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        booking.status = new_status
        booking.save()
        return redirect('admin_dashboard')
    
    return render(request, 'change_status.html', {'booking': booking})


from django.shortcuts import render, get_object_or_404
from .models import Booking

def ownerpf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'admin_showprofile.html', {'booking': booking})

def petpf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'admin_petprofile.html', {'booking': booking})



def PetprofilePage(request):
    try:
        owner_instance = Owner.objects.get(user=request.user)
    except Owner.DoesNotExist:
        messages.error(request, 'pls create a owner profile first')
        return redirect ('profile')
    
    pet_instances = Pet.objects.filter(owner=owner_instance)

    if not pet_instances:
        pet_instance = None
    else:
        pet_instance = pet_instances.first()

    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet_instance)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = owner_instance
            pet.save()
            # form.save()
            messages.success(request, f'profile has been updated')
            return redirect('petprofile')
    else:
        form = PetForm(instance=pet_instance)

    context = {'form':form}
    return render(request, 'petprofile.html', context)


def profilePage(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        o_form = OwnerUpdateForm(request.POST, request.FILES, instance=request.user.owner)
        if u_form.is_valid() and o_form.is_valid():
            u_form.save()
            o_form.save()
            messages.success(request, f'profile has been updated')
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






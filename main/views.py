from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django import forms
from .forms import CreateUserForm, UserUpdateForm, OwnerUpdateForm, PetForm, BookingForm
from .models import Pet, Owner, Booking, Room
from django.urls import reverse
from django.views.generic.edit import UpdateView
from .forms import BookingForm
import datetime
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from .models import Booking, Owner
from .forms import BookingForm, RoomForm

# def room_list(request):
#     rooms = Room.objects.all()
#     room_id_1 = get_object_or_404(Room, pk=1)  # Fetch room with id=1
#     return render(request, 'room_list.html', {'room_id_1': room_id_1, 'rooms': rooms})

    
def AdminPage(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        
        if booking_id and new_status:
            booking = get_object_or_404(Booking, id=booking_id)
            if new_status in ['Ongoing', 'Completed', 'Cancelled']:
                booking.status = new_status
                booking.save()
    
    sort_by = request.GET.get('sort_by', 'date')

    order_by = '-date'  # default ordering
    if sort_by == 'id':
        order_by = 'id'
    elif sort_by == 'service':
        order_by = 'service'

    ongoing_bookings = Booking.objects.filter(status='Ongoing').order_by(order_by)
    completed_bookings = Booking.objects.filter(status='Completed').order_by(order_by)
    cancelled_bookings = Booking.objects.filter(status='Cancelled').order_by(order_by)

    owners = Owner.objects.all()
    context = {
        'ongoing_bookings': ongoing_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'owners': owners,
        'rooms': rooms,
    }
    return render(request, 'admin_dashboard.html', context)

class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'edit_booking.html'

    def get_object(self):
        booking_id = self.kwargs.get('pk')
        return get_object_or_404(Booking, id=booking_id)

    def form_valid(self, form):
        form.save()
        return redirect('admin_dashboard')


def BookingPage(request):
    owner = request.user.owner

    if request.method == 'POST':
        form = BookingForm(owner, request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = owner

            if booking.service == 'Pet Hotel':
                booking.date = None
                booking.time = None
                # Check room availability only for Pet Hotel
                available_rooms = Room.objects.all()
                for room in available_rooms:
                    overlapping_bookings = Booking.objects.filter(
                        room=room,
                        checkin__lte=booking.checkout,
                        checkout__gte=booking.checkin,
                        service='Pet Hotel'  # Check only for Pet Hotel service
                    ).exists()
                    if not overlapping_bookings:
                        booking.room = room
                        break
                else:
                    messages.error(request, "No rooms are available for the selected dates.")
                    context = {'form': form, 'bookings': Booking.objects.filter(owner=owner)}
                    return render(request, 'bookingpage.html', context)
            else:
                booking.checkin = None
                booking.checkout = None

            booking.save()
            form.save_m2m()
            messages.success(request, 'Booking has been updated')
            context = {'form': form, 'booking': booking}
            return render(request, 'bookingpage.html', context)
        else:
            print(form.errors)
    else:
        form = BookingForm(owner)
    
    bookings = Booking.objects.filter(owner=owner)
    context = {'form': form, 'bookings': bookings}
    return render(request, 'bookingpage.html', context)

def update_times(request):
    service = request.GET.get('service')
    date = request.GET.get('date')
    
    form = BookingForm(request.user.owner, initial={'service': service, 'date': date})
    available_times = form.get_available_time_choices(date, service)
    
    return JsonResponse({'available_times': dict(available_times)})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm

def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    owner = booking.owner
    owner_pets = Pet.objects.filter(owner=owner)

    if request.method == 'POST':
        form = BookingForm(owner, request.POST, instance=booking)
        if form.is_valid():
            booking_instance = form.save(commit=False)

            if booking_instance.service == 'Pet Hotel':
                booking_instance.date = None
                booking_instance.time = form.cleaned_data['time']

                available_rooms = Room.objects.all()
                room_assigned = False
                booking_instance.save()
                for room in available_rooms:
                    overlapping_bookings = Booking.objects.filter(
                        room=room,
                        checkin__lte=booking_instance.checkout,
                        checkout__gte=booking_instance.checkin,
                        service='Pet Hotel'  # Check only for Pet Hotel service
                    ).exists()
                    if not overlapping_bookings:
                        booking_instance.room = room
                        room_assigned = True
                        break
                booking_instance.save()
                if not room_assigned:
                    messages.error(request, "No rooms are available for the selected dates.")
                    context = {'form': form, 'bookings': Booking.objects.filter(owner=owner)}
                    return render(request, 'bookingpage.html', context)

            else:
                booking_instance.checkin = None
                booking_instance.checkout = None

            # Save the changes to the database
            booking_instance.save()

            messages.success(request, 'Booking has been updated successfully.')
            return redirect('admin_dashboard')  # Redirect to admin dashboard after successful update
    else:
        form = BookingForm(owner, instance=booking)

    return render(request, 'edit_booking.html', {'form': form, 'booking': booking, 'owner_pets': owner_pets})




from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from .models import Booking
from .forms import BookingForm
from django.http import JsonResponse 


def ownerpf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    pets = booking.pet.all()
    print(pets)  # Debug output
    return render(request, 'admin_showprofile.html', {'booking': booking, 'pets': pets})

# def petpf(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     return render(request, 'admin_petprofile.html', {'booking': booking})
from django.shortcuts import render
from.models import Booking
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking
import json


def timetable(request):
    bookings = Booking.objects.all()
    context = {
        "bookings": bookings,
    }
    return render(request, 'timetable.html', context)


def update_booking(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        start_str = request.POST.get('start')
        end_str = request.POST.get('end')

        try:
            event = Booking.objects.get(id=event_id)
            start_dt = datetime.datetime.strptime(start_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            end_dt = datetime.datetime.strptime(end_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            event.start = start_dt
            event.end = end_dt
            event.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

from django.http import JsonResponse
from.models import Booking
from django.http import JsonResponse
from .models import Booking

def get_booking(request):
    bookings = Booking.objects.all()  # Retrieve all bookings from the database
    events = []
    for booking in bookings:
        if booking.service == 'Hair Grooming':
            event = {
                "title": booking.service,
                "start": f"{booking.date}T{booking.time}",
                "color": "green",
                "id": booking.id,
                'owner': booking.owner.user.username
            }
            events.append(event)

        elif booking.service == 'Bath and Dry':
            event = {
                "title": booking.service,
                "start": f"{booking.date}T{booking.time}",
                "color": "light blue",
                "id": booking.id,
                'owner': booking.owner.user.username
            }
            events.append(event)

        elif booking.service == 'Pet Daycare':
            if booking.time == 'full_day':
                events.append({
                    'title': f'{booking.owner.user.username} - full ({booking.id})',
                    'tart': booking.date,
                    'end': booking.date,
                    'owner': booking.owner.user.username,
                    'allDay': True,
                    'color' : 'orange',
                    'description': f'Service: {booking.service}\nStatus: {booking.status}',
                })

            elif booking.time == 'morning':
                events.append({
                    'title': f'{booking.owner.user.username} - morning ({booking.id})',
                    'tart': booking.date,
                    'end': booking.date,
                    'owner': booking.owner.user.username,
                    'allDay': True,
                    'color' : 'green',
                    'description': f'Service: {booking.service}\nStatus: {booking.status}',
                })

            elif booking.time == 'noon':
                events.append({
                    'title': f'{booking.owner.user.username} - noon ({booking.id})',
                    'tart': booking.date,
                    'end': booking.date,              
                    'color' : 'blue',
                    'owner': booking.owner.user.username,
                    'allDay': True,
                    'description': f'Service: {booking.service}\nStatus: {booking.status}',
                })

    return JsonResponse(events, safe=False)


# def get_booking(request):
#     bookings = Booking.objects.all()

#     events = []
#     for booking in bookings:
#         if booking.service == 'Hair Grooming':
#             color = 'green'
#         elif booking.service == 'Bath and Dry':
#             color = 'light blue'
#         elif booking.service == 'Pet Daycare':
#             if booking.time == 'full_day':
#                 events.append({
#                     'title': f'{booking.owner.user.username} - full ({booking.id})',
#                     'start': booking.date,
#                     'end': booking.date,
#                     'allDay': True,
#                     'color': 'orange',
#                     'description': f'Service: {booking.service}\nStatus: {booking.status}',
#                 })
#             elif booking.time == 'morning':
#                 events.append({
#                     'title': f'{booking.owner.user.username} - morning ({booking.id})',
#                     'start': booking.date,
#                     'end': booking.date,
#                     'allDay': True,
#                     'color': 'green',
#                     'description': f'Service: {booking.service}\nStatus: {booking.status}',
#                 })
#             elif booking.time == 'noon':
#                 events.append({
#                     'title': f'{booking.owner.user.username} - noon ({booking.id})',
#                     'start': booking.date,
#                     'end': booking.date,
#                     'color': 'blue',
#                     'allDay': True,
#                     'description': f'Service: {booking.service}\nStatus: {booking.status}',
#                 })
#             else:
#                 events.append({
#                     'title': f'{booking.owner.user.username} - {booking.time} ({booking.id})',
#                     'start': booking.date,
#                     'end': booking.date,
#                     'allDay': True,
#                     'color': 'purple',
#                     'description': f'Service: {booking.service}\nStatus: {booking.status}',
#                 })
#         else:
#             events.append({
#                 'title': f'{booking.owner.user.username} - {booking.service} ({booking.id})',
#                 'start': f"{booking.date}T{booking.time}",
#                 'color': 'gray',
#                 'description': f'Service: {booking.service}\nStatus: {booking.status}',
#             })

#     return JsonResponse(events, safe=False)

# @csrf_exempt
# @require_POST
# def update_booking(request):
#     try:
#         data = request.POST
#         event_id = data.get('id')
#         start = data.get('start')
#         end = data.get('end')

#         # Log incoming data
#         print('Received data:', event_id, start, end)

#         event = Booking.objects.get(id=event_id)
#         event.start = start
#         event.end = end
#         event.save()

#         return JsonResponse({'success': True})
#     except Booking.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Event not found'})
#     except Exception as e:
#         print('Error updating event:', str(e))
#         return JsonResponse({'success': False, 'error': str(e)})

def save_changes(request):
    if request.method!= 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    events = {}
    for key, value in request.POST.items():
        if key.startswith('id_'):
            event_id = int(key.split('_')[1])
            events[event_id] = {}
        elif key.startswith('start_'):
            event_id = int(key.split('_')[1])
            events[event_id]['start'] = value
        elif key.startswith('end_'):
            event_id = int(key.split('_')[1])
            events[event_id]['end'] = value

    for event_id, event_data in events.items():
        try:
            booking = Booking.objects.get(id=event_id)
            booking.start = event_data['start']
            if 'end' in event_data:
                booking.end = event_data['end']
            else:
                booking.end = None
            booking.save()
        except Booking.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Booking not found'})

    return JsonResponse({'success': True})


def CalendarPage(request):
    owner = request.user.owner
    bookings = Booking.objects.filter(owner=owner, )
    context = {
        "bookings": bookings,
    }
    return render(request, 'calendar.html', context)

def all_bookings(request):
    owner = request.user.owner
    bookings = Booking.objects.filter(owner=owner)
    out = []
    for booking in bookings:
        if booking.service in ['Hair Grooming', 'Bath and Dry','Pet Daycare']:
            if booking.date and booking.time:
                pets = booking.pet.all()  # Fetch all pets associated with this booking
                pet_names = ', '.join([pet.name for pet in pets])
                color = '#FF6347' if booking.service == 'Hair Grooming' else '#4682B4' if booking.service == 'Bath and Dry' else '#f0e130'

                out.append({
                    'title': booking.service,
                    'id': booking.id,
                    'start': booking.date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'allDay': True,
                    'color': color,
                    'details': {
                        'id': booking.id,
                        'Date': booking.date.strftime("%Y-%m-%d"),
                        'Time': booking.time,
                        'Service': booking.service,
                        'Pets': pet_names,
                    }
                })
        elif booking.service in ['Pet Hotel']:
            if booking.checkin and booking.checkout:
                room_data = {
                    'name': booking.room.name,  # Example: Assuming 'room' has a 'name' field
                }
                pets = booking.pet.all()  # Fetch all pets associated with this booking
                pet_names = ', '.join([pet.name for pet in pets])                
                end_date = booking.checkout + timedelta(days=1)  # Adjust end date to be exclusive
                out.append({
                    'title': booking.service,
                    'id': booking.id,
                    'start': booking.checkin.strftime("%Y-%m-%dT%H:%M:%S"),
                    'end': end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'allDay': True,
                    'color': '#32CD32' ,  # Different colors
                    'details': {
                        'id': booking.id,
                        'Checkin': booking.checkin.strftime("%Y-%m-%d"),
                        'Checkout': booking.checkout.strftime("%Y-%m-%d"),
                        'Service': booking.service,
                        'Room': room_data,
                        'Pets': pet_names,
                    }
                })

    return JsonResponse(out, safe=False)

def room_detail(request, room_id=None):
    room = get_object_or_404(Room, pk=room_id) if room_id else None
    rooms = Room.objects.all()

    context = {
        'room': room,
        'rooms': rooms,
    }

    return render(request, 'room_detail.html', context)

def get_room_events(request, room_id):
    bookings = Booking.objects.filter(room_id=room_id, service='Pet Hotel')

    events = []
    for booking in bookings:
        start_time = booking.checkin.strftime("%Y-%m-%dT%H:%M:%S") if booking.checkin else None
        end_date = booking.checkout + timedelta(days=1)  # Adjust end date to be exclusive
        pets = booking.pet.all()  # Fetch all pets associated with this booking
        pet_names = ', '.join([pet.name for pet in pets]) 
        room_data = {
            'name': booking.room.name,  # Example: Assuming 'room' has a 'name' field
        }

        title = f"Booking ID: {booking.id} - {pet_names}"   
        
        events.append({
            'id': booking.id,
            'title': title,
            'start': start_time,
            'end': end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            'allDay': True,
            'color': '#32CD32',
            'details': {
                'id': booking.id,
                'Checkin': booking.checkin.strftime("%Y-%m-%d"),
                'Checkout': booking.checkout.strftime("%Y-%m-%d"),
                'Room': room_data,
                'Pets': pet_names,
                'Owner' : booking.owner.user.username,
                'ContactNumber' : booking.owner.phone_number

                # Add more details as needed
            }


        })

    return JsonResponse(events, safe=False)

def PetprofilePage(request):
    try:
        owner_instance = Owner.objects.get(user=request.user)
    except Owner.DoesNotExist:
        messages.error(request, 'pls create a owner profile first')
        return redirect ('profile')
    pet_instances = Pet.objects.filter(owner=owner_instance)
    # if not pet_instances:
    #     pet_instance = None
    # else:
    #     pet_instance = pet_instances.first()
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = owner_instance
            pet.save()
            form.save_m2m()

            # form.save()
            messages.success(request, f'profile has been updated')
            return redirect('petprofile')
    else:
        form = PetForm()

    context = {'form':form, 'pet_instances': pet_instances}
    return render(request, 'petprofile.html', context)

def edit_pet(request, pet_id):
    pet_instance = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet_instance)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.save()
            return redirect('edit_pet',pet_id=pet_id)
        
    else:
        form = PetForm(initial={
            'name': pet_instance.name,
            'owner': pet_instance.owner,
            'age': pet_instance.age,
            'species': pet_instance.species,
            'breed': pet_instance.breed,
            'profile_pic':pet_instance.profile_pic
        })

    context = {
        'form': form, 
        'pet_instance': pet_instance
    }
    return render(request, 'edit_pet.html', context)
        

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
                user = form.save()
                username = form.cleaned_data.get('username')
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

@login_required
def customer_booking(request):
    owner = request.user.owner
    bookings = Booking.objects.filter(owner=owner, )
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'customer_booking.html', context)
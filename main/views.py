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
from datetime import datetime, time, timedelta
from django.utils import timezone
from django.utils.timezone import now, localtime
from django.shortcuts import render, get_object_or_404


def generate_time_slots(start_time, end_time, slot_duration):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time.strftime("%H:%M"))
        current_time += slot_duration
    return slots

def get_week_dates(offset=0):
    today = localtime(now()).date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week += timedelta(weeks=offset)
    return [start_of_week + timedelta(days=i) for i in range(6)]  # Monday to Saturday

def timetable(request):
    if request.method == 'POST':
        week_offset = int(request.POST.get('week_offset', 0))
    else:
        week_offset = int(request.GET.get('week_offset', 0))

    week_dates = get_week_dates(week_offset)
    timetable = []
    hours = generate_time_slots(datetime.strptime("09:00", "%H:%M"), datetime.strptime("18:00", "%H:%M"), timedelta(hours=1))

    for day in week_dates:
        day_schedule = []
        for hour in hours:
            slot_datetime = datetime.combine(day, datetime.strptime(hour, "%H:%M").time())
            booking = Booking.objects.filter(date=day, time=slot_datetime.time()).first()

            is_available = booking is None
            day_schedule.append((slot_datetime, is_available, booking))
        timetable.append((day, day_schedule))

    context = {
        'timetable': timetable,
        'week_offset': week_offset,
        'display_monday': week_dates[0],
        'display_today': localtime().date(),
        'hours': hours,
    }
    return render(request, 'timetable.html', context)





from datetime import datetime, time, timedelta
from django.utils import timezone
from django.utils.timezone import now, localtime

from django.shortcuts import render
from django.utils.timezone import localtime
from datetime import datetime, timedelta
from .models import Booking

def get_week_dates(week_offset):
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    return [start_of_week + timedelta(days=i) for i in range(7)]

def generate_time_slots(start, end, delta):
    times = []
    while start < end:
        times.append(start.strftime('%H:%M'))
        start += delta
    return times

def timetable(request):
    if request.method == 'POST':
        week_offset = int(request.POST.get('week_offset', 0))
    else:
        week_offset = int(request.GET.get('week_offset', 0))

    week_dates = get_week_dates(week_offset)
    timetable = []
    hours = generate_time_slots(datetime.strptime("09:00", "%H:%M"), datetime.strptime("18:00", "%H:%M"), timedelta(hours=1))

    for day in week_dates:
        day_schedule = []
        for hour in hours:
            slot_time = datetime.combine(day, datetime.strptime(hour, "%H:%M").time())
            booking = Booking.objects.filter(date=day, time=slot_time.time(), service__in=['Hair Grooming', 'Bath and Dry']).first()

            is_available = booking is None
            day_schedule.append((slot_time, is_available, booking))
        timetable.append((day, day_schedule))
    bookings = Booking.objects.filter(service__in=['Hair Grooming', 'Bath and Dry']).order_by('date', 'time')
    timetable = {}
    for booking in bookings:
        date = booking.date
        time = booking.time.strftime('%H:%M')
        if date not in timetable:
            timetable[date] = {}
        timetable[date][time] = booking
    hours = sorted(set(booking.time.strftime('%H:%M') for booking in bookings))


    context = {
        'timetable': timetable,
        'bookings':bookings,
        'week_offset': week_offset,
        'display_monday': week_dates[0],
        'display_today': localtime().date(),
        'hours': hours,
    }
    return render(request, 'timetable.html', context)




def AdminPage(request):
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

            if booking.service in ['Pet Hotel', 'Pet Daycare']:
                booking.date = None
                booking.time = None
            else:
                booking.checkin = None
                booking.checkout = None

            available_rooms = Room.objects.all()
            for room in available_rooms:
                overlapping_bookings = Booking.objects.filter(
                    room=room,
                    checkin__lte=booking.checkout,
                    checkout__gte=booking.checkin
                ).exists()
                if not overlapping_bookings:
                    booking.room = room
                    break
            else:
                messages.error(request, "No rooms are available for the selected dates.")
                context = {'form': form, 'bookings': Booking.objects.filter(owner=owner)}
                return render(request, 'bookingpage.html', context)            

            booking.save()
            form.save_m2m()
            messages.success(request, f'Booking has been updated')
            context = {'form': form, 'booking': booking}
            return render(request, 'bookingpage.html', context)
        else:
            print(form.errors)
    else:
        form = BookingForm(owner)
    bookings = Booking.objects.filter(owner=owner)

    context = {'form': form, 'bookings': bookings}
    return render(request, 'bookingpage.html', context)



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
            if booking_instance.service in ['Pet Hotel', 'Pet Daycare']:
                booking_instance.date = None
                booking_instance.time = None
            else:
                booking_instance.checkin = None
                booking_instance.checkout = None
            booking_instance.save()
            return redirect('admin_dashboard')
    else:
        form = BookingForm(owner, instance=booking)
    
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking, 'owner_pets': owner_pets})




from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from .models import Booking
from .forms import BookingForm




from django.shortcuts import render, get_object_or_404
from .models import Booking

def ownerpf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    pets = booking.pet.all()
    print(pets)  # Debug output
    return render(request, 'admin_showprofile.html', {'booking': booking, 'pets': pets})

# def petpf(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)
#     return render(request, 'admin_petprofile.html', {'booking': booking})



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
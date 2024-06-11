from django.urls import path 
from . import views
from .views import AdminPage, BookingUpdateView
urlpatterns = [
    path('admin_dashboard/', views.AdminPage, name="admin_dashboard"),
    path('timetable/', views.timetable, name="timetable"),
    path('get_booking/', views.get_booking, name="get_booking"),
    path('profile/', views.profilePage, name="profile"),
    path('petprofile/', views.PetprofilePage, name="petprofile"),
    path('edit_pet/<int:pet_id>', views.edit_pet, name="edit_pet"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('bookingpage/', views.BookingPage, name="bookingpage"),
    path('update_times/', views.update_times, name='update_times'),    
    path('calendar/', views.CalendarPage, name="calendar"),    
    path('all_bookings/', views.all_bookings, name="all_bookings"),    
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('create_room/', views.create_room, name='create_room'),
    path('resize_booking/', views.resize_booking, name="resize_booking"),    
    path('update_booking_dates/', views.update_booking_dates, name="update_booking_dates"),    
    path('get_room_events/<int:room_id>/', views.get_room_events, name='get_room_events'),    
    path('',views.home, name="home"),
    path('edit-booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('ownerprofile/<int:booking_id>/', views.ownerpf, name='ownerpf'),
    path('customer_booking/', views.customer_booking, name='customer_booking'),
]

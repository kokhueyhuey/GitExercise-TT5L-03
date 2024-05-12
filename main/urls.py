from django.urls import path 
from . import views

urlpatterns = [
    path('admin_dashboard/', views.AdminPage, name="admin_dashboard"),
    path('profile/', views.profilePage, name="profile"),
    path('petprofile/', views.PetprofilePage, name="petprofile"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('bookingpage/', views.BookingPage, name="bookingpage"),
    path('',views.home, name="home"),
]

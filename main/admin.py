from django.contrib import admin
from .models import Owner, Pet, Booking

# Register your models here.

# admin.site.register(Owner)
@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id','user','email','phone_number')
    ordering = ('id',)


# admin.site.register(Pet)
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('id','name','owner')
    ordering = ('id',)

    
# admin.site.register(Booking)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','owner','get_pets','date','time','service', 'status')

def get_pets(self, obj):
    return ", ".join([pet.name for pet in obj.pet.all()])
get_pets.short_description = 'Pets'

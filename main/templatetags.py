
from django import template
from main.models import Booking

register = template.Library()

@register.filter(name='get_hourly_booking')
def get_hourly_booking(day_schedule, hour):
    # Retrieve booking for the given hour from the day_schedule
    bookings = day_schedule.filter(time__hour=hour)
    return bookings

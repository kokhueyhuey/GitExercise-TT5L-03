
from django import template
from main.models import Booking

register = template.Library()

@register.filter
def get_value(dict, key):
    return dict.get(key)

@register.filter
def initialize_list(value):
    return []

@register.simple_tag
def filter_bookings_by_date_and_time(slots, date, time):
    def filter_func(bookings):
        return [booking for booking in bookings if booking.date == date and booking.time == time]
    return filter_func(slots)
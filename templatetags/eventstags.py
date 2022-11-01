from django import template
from django.template import defaultfilters

register = template.Library()


@register.filter
def eventsdate(date):
    return defaultfilters.date(date, "d.m.Y в H:i")

@register.filter
def reviewsdate(date):
    return defaultfilters.date(date, "d.m.Y")

@register.filter
def occupancy_percent(number):
    return int(number * 100)

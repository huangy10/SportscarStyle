from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from .models import Sportscar


@register(Sportscar)
class SportscarAdmin(admin.ModelAdmin):
    exclude = ("remote_id", 'price_number', 'remote_image', 'remote_thumbnail', 'data_fetched')
    list_display = ('name', 'price', 'fuel_consumption', 'engine', 'transmission', 'max_speed', 'torque')

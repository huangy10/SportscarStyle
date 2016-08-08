from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from .models import News


@register(News)
class NewsAdmin(admin.ModelAdmin):
    exclude = ("liked_by", "shared_times", "created_at", )
    search_fields = ('title', )

from bs4 import BeautifulSoup

from django.contrib import admin

# Register your models here.
from django.contrib.admin import register
from .models import News


@register(News)
class NewsAdmin(admin.ModelAdmin):
    exclude = ("liked_by", "shared_times", "created_at", )
    search_fields = ('title', )

    def save_model(self, request, obj, form, change):
        if obj.is_video:
            link = obj.content
            try:
                src = BeautifulSoup(link).find("iframe")["src"]
                obj.content = src
            except TypeError:
                pass
        super(NewsAdmin, self).save_model(request, obj, form, change)

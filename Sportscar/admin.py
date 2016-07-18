from django.contrib import admin
from django.core.urlresolvers import reverse

# Register your models here.
from django.contrib.admin import register
from .models import Sportscar, SportCarIdentificationRequestRecord, SportCarOwnership


@register(Sportscar)
class SportscarAdmin(admin.ModelAdmin):
    exclude = ("remote_id", 'price_number', 'remote_image', 'remote_thumbnail', 'data_fetched')
    list_display = ('name', 'price', 'fuel_consumption', 'engine', 'transmission', 'max_speed', 'torque')
    search_fields = ("name", )


@register(SportCarIdentificationRequestRecord)
class SportCarIdentificationRequestRecordAdmin(admin.ModelAdmin):
    search_fields = ("license_num", )

    def link_to_user(self, obj):
        link = reverse("admin:user_user_change", args=obj.ownership.user.id)
        return u'<a href="%s">%s(%s)</a>' % (link, obj.ownership.user.name, obj.ownership.user.username)

    fields = ("ownership", "created_at", "approved",
              "drive_license_admin", "id_card_admin", "photo_admin", "license_num",
              link_to_user, )



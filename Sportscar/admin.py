# coding=utf-8
from django.contrib import admin
from django.core.urlresolvers import reverse

# Register your models here.
from django.contrib.admin import register
from django.utils import timezone

from .models import Sportscar, SportCarIdentificationRequestRecord, SportCarOwnership


@register(Sportscar)
class SportscarAdmin(admin.ModelAdmin):
    exclude = ("remote_id", 'price_number', 'remote_image', 'remote_thumbnail', 'data_fetched')
    list_display = ('name', 'price', 'fuel_consumption', 'engine', 'transmission', 'max_speed', 'torque')
    search_fields = ("name", )


class SportCarOwnershipInlineAdmin(admin.StackedInline):

    model = SportCarOwnership


@register(SportCarIdentificationRequestRecord)
class SportCarIdentificationRequestRecordAdmin(admin.ModelAdmin):
    search_fields = ("license_num", )

    # def link_to_user(self, obj):
    #     return u'<a href="/admin/User/user/%s">%s(%s)</a>' % (obj.ownership.user.id, obj.ownership.user.nick_name,
    #                                                           obj.ownership.user.username)
    # link_to_user.short_description = u'申请人'
    # link_to_user.allow_tags = True

    # fields = ("ownership", "created_at", "approved",
    #           "drive_license_admin", "id_card_admin", "photo_admin", "license_num",
    #           "link_to_user", )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    fields = ("link_to_user", "link_to_car", "license_num","approved", "checked", "drive_license_admin", "id_card_admin",
              "photo_admin", "created_at", )
    exclude = None
    readonly_fields = ("link_to_user", "drive_license_admin", "id_card_admin", "photo_admin", "created_at",
                    "link_to_car", "license_num")
    list_display = ("created_at", "link_to_user", "link_to_car", "checked", "approved")
    list_filter = ("checked", "approved")

    def save_model(self, request, obj, form, change):
        old_obj = SportCarIdentificationRequestRecord.objects.get(id=obj.id)
        if not old_obj.checked and obj.checked:
            own = obj.ownership
            own.identified = obj.approved
            own.identified_at = timezone.now()
            own.save()
            print "AUTH"
        super(SportCarIdentificationRequestRecordAdmin, self)\
            .save_model(request, obj, form, change)

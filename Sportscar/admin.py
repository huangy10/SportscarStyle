# coding=utf-8
from bs4 import BeautifulSoup

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

# Register your models here.
from django.contrib.admin import register
from django.utils import timezone
from django.forms.models import BaseInlineFormSet

from .models import Sportscar, SportCarIdentificationRequestRecord, SportCarOwnership, Manufacturer, CarMediaItem
from .models import MAX_AUDIO_PER_CAR, MAX_IMAGE_PER_CAR, MAX_VIDEO_PER_CAR


class SportscarInlineAdmin(admin.StackedInline):

    model = Sportscar
    exclude = ("remote_id", 'price_number', 'remote_image', 'remote_thumbnail', 'data_fetched')
    extra = 1
    show_change_link = True


class CarMediaItemFormset(BaseInlineFormSet):

    def clean(self):
        super(CarMediaItemFormset, self).clean()
        image_num = 0
        video_num = 0
        audio_num = 0
        for form in self.forms:
            if not form.is_valid():
                continue
            if form.cleaned_data["DELETE"]:
                continue
            item_type = form.cleaned_data.get("item_type", None)
            if item_type == "image":
                image_num += 1
            elif item_type == "video":
                video_num += 1
            elif item_type == "audio":
                audio_num += 1
            else:
                raise ValidationError(message=u"没有定义的附件类型")

        if image_num > MAX_IMAGE_PER_CAR:
            raise ValidationError(message=u"最多只允许%s张图片" % MAX_IMAGE_PER_CAR)
        if video_num > MAX_VIDEO_PER_CAR:
            raise ValidationError(message=u"最多只允许%s个视频" % MAX_VIDEO_PER_CAR)
        if audio_num > MAX_AUDIO_PER_CAR:
            raise ValidationError(message=u'最多只允许%s个音频' % MAX_AUDIO_PER_CAR)

    def save(self, commit=True):
        items = super(CarMediaItemFormset, self).save(commit=False)
        for item in items:
            if item.item_type == "video":
                link = item.link
                try:
                    src = BeautifulSoup(link).find("iframe")["src"]
                    item.link = src
                except TypeError:
                    pass
            if commit:
                item.save()
        if commit:
            for delete_obj in self.deleted_objects:
                delete_obj.delete()
        return items


class CarMediaItemAdmin(admin.TabularInline):

    model = CarMediaItem
    formset = CarMediaItemFormset
    extra = 0
    readonly_fields = ("created_at", )


@register(Sportscar)
class SportscarAdmin(admin.ModelAdmin):
    exclude = ("remote_id", 'price_number', 'remote_image', 'remote_thumbnail', 'data_fetched', "image", "thumbnail")
    list_display = ('name', 'price', 'fuel_consumption', 'engine', 'transmission', 'max_speed', 'torque')
    search_fields = ("name", )

    inlines = (CarMediaItemAdmin, )


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

    fields = ("link_to_user", "link_to_car", "license_num", "approved", "checked", "drive_license_admin",
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
            user = own.user
            if own.identified and user.avatar_car is None:
                user.avatar_car = own
                user.save()
            own.save()
        super(SportCarIdentificationRequestRecordAdmin, self)\
            .save_model(request, obj, form, change)


@register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    exclude = ('remote_id', 'detail_url', 'logo_remote', )
    list_display = ('name', 'index', )
    search_fields = ('name', 'index', )

    inlines = [SportscarInlineAdmin, ]


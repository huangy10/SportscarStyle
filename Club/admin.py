# coding=utf-8
from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from Club.models import Club, ClubAuthRequest
# Register your models here.


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):

    exclude = ('deleted', 'members')
    list_display = ('name', 'id', "description", "identified", "created_at", "value_total", "value_average",
                    "members_num")
    list_filter = ('identified', )
    readonly_fields = ("value_total", "value_average", )

    def get_queryset(self, request):
        qs = super(ClubAdmin, self).get_queryset(request)
        return qs.annotate(members_num=Count("members"))

    def members_num(self, obj):
        return obj.members_num
    members_num.short_description = u"成员数量"
    members_num.admin_order_field = "members_count"


@admin.register(ClubAuthRequest)
class ClubAuthRequestAdmin(admin.ModelAdmin):

    fields = ("approve", "checked", "city", "description", "club_link")
    readonly_fields = ("city", "description", "club_link")
    list_display = ("club", "description", "city", "approve", "checked")
    list_filter = ('checked', "approve")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        old_obj = ClubAuthRequest.objects.get(id=obj.id)
        if not old_obj.checked and obj.checked:
            club = obj.club
            club.identified = True
            club.identified_at = timezone.now()
            club.save()
        super(ClubAuthRequestAdmin, self).save_model(request, obj, form, change)

    def club_link(self, obj):
        return u'<a href="/admin/Club/club/%s">%s</a>' % (obj.club.id, obj.club.name)
    club_link.short_description = u'申请俱乐部'
    club_link.allow_tags = True

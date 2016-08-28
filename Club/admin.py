# coding=utf-8
from django.contrib import admin
from django.db.models import Count

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

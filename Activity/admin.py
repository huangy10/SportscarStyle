import excel_response

from django.conf.urls import url
from django.contrib import admin

from .models import Activity
# Register your models here.


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = ("location", "like_num", "comment_num", )
    exclude = ("liked_by", )

    def export_to_excel(self, request, act_id):
        act = Activity.objects.get(id=act_id)
        data = act.export_to_excel()
        return excel_response.ExcelResponse(data, output_name=act.name.encode("utf-8"))

    def get_urls(self):
        urls = super(ActivityAdmin, self).get_urls()
        extended_urls = [
            url(r'^act/(?P<act_id>\d+)/excel', self.export_to_excel, name='act_excel')
        ]
        return urls + extended_urls

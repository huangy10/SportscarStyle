# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators import http as http_decorators
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from custom.utils import login_first, page_separator_loader
from .models import Notification
# Create your views here.


@http_decorators.require_GET
@login_first
@page_separator_loader
def notification_list(request, date_threshold, op_type, limit):
    """ 获取当前用户相关的所有消息内容,复合标准的分页参数标准
     :param date_threshold  时间分割阈值
     :param op_type         操作类型,more/latest
     :param limit           最大获取的条目数量
    """
    date_fix = request.GET.get("date_fix", None)
    if date_fix is not None and date_fix != "":
        try:
            date_fix = Notification.objects.get(id=date_fix).created_at
            date_threshold = date_fix
        except ObjectDoesNotExist:
            pass
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    notif = Notification.objects.select_related(
        "related_user__profile",
        "related_club",
        "related_act",
        "related_status",
        "related_status_comment",
        "related_news",
        "related_news_comment"
    ).order_by("-created_at").filter(date_filter, target=request.user)[0:limit]
    return JsonResponse(
        dict(success=True, notifications=map(lambda x: x.dict_description(), notif)))


@http_decorators.require_POST
@login_first
def notification_mark_read(request, notif_id):
    """ 将给定的消息标记为已读
    """
    try:
        notif = Notification.objects.get(id=notif_id, target=request.user)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code="7000", message="Notification Not Found"))
    notif.read = True
    notif.save()
    return JsonResponse(dict(success=True))


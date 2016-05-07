# coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators import http as http_decorators
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from custom.utils import login_first, page_separator_loader
from .models import Notification
from .tasks import clear_notification_unread_num
# Create your views here.


@http_decorators.require_GET
@login_first
def notification_list(request):
    """ 获取当前用户相关的所有消息内容
    """
    skips = int(request.GET["skips"])
    limit = int(request.GET["limit"])

    notif = Notification.objects.select_related(
        "related_user__profile",
        "related_club",
        "related_act",
        "related_status",
        "related_status_comment",
        "related_news",
        "related_news_comment"
    ).order_by("-created_at").filter(target=request.user)[skips:(limit + skips)]
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


@http_decorators.require_POST
@login_first
def notification_clear(request):
    clear_notification_unread_num.delay(request.user)
    return JsonResponse(dict(success=True))

# coding=utf-8
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from custom.utils import login_first, page_separator_loader
from .models import ChatRecordBasic
from Club.models import Club
# Create your views here.


@require_GET
@login_first
def chat_list(request):
    """ 暂时先返回所有的聊天单元
     返回的信息包括每个单元的类型(private/group),目标信息(target_user/target_club),以及最近的一条聊天的内容
    """
    result = ChatRecordBasic.objects.select_related("sender__profile", "target_club")\
        .order_by("distinct_identifier", "-created_at")\
        .filter(Q(target_user=request.user) | Q(target_club__members=request.user), deleted=False)\
        .distinct("distinct_identifier")
    print(result)
    return JsonResponse(dict(success=True, data=map(lambda x: x.dict_description(), result)))

@require_GET
@login_first
@page_separator_loader
def historical_record(request, date_threshold, op_type, limit):
    """ 获取历史聊天信息
     :param op_type only accept "more"
    """
    if op_type != "more":
        return JsonResponse(
                dict(success=False, code="3400", message="op_type invalid")
        )
    target_id = request.GET["target_id"]
    chat_type = request.GET["chat_type"]

    if chat_type == "private":
        try:
            target_user = get_user_model().objects.get(id=target_id)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code="3002", message="User not found"))
        target_filter = Q(target_user=target_user)
    elif chat_type == "group":
        try:
            # 用户必须是俱乐部的成员才能获取历史信息
            target_club = Club.objects.get(id=target_id, members=request.user)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code="2002", message="club not found"))
        target_filter = Q(target_club=target_club)
    else:
        return JsonResponse(dict(success=False, code="6002", message="invalid chat type"))

    result = ChatRecordBasic.objects.filter(
        target_filter,
        created_at__lt=date_threshold,
        chat_type=chat_type,
        deleted=False
    )
    result.update(read=True)
    return JsonResponse(dict(
            success=True, chats=map(lambda x: x.dict_description(), result)))

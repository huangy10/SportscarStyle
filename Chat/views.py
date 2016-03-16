# coding=utf-8
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from django.db.models import Q, Count, F, Case, When, Sum
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from custom.utils import login_first, page_separator_loader, post_data_loader
from .models import ChatRecordBasic
from Club.models import Club, ClubJoining
from Profile.models import UserRelationSetting
# Create your views here.


@require_GET
@login_first
def chat_list(request):
    """ 暂时先返回所有的聊天单元
     返回的信息包括每个单元的类型(private/group),目标信息(target_user/target_club),以及最近的一条聊天的内容
    """
    result = ChatRecordBasic.objects.select_related("sender__profile", "target_club")\
        .order_by("distinct_identifier", "-created_at")\
        .filter(
            Q(target_user=request.user) |
            Q(target_club__members=request.user) |
            Q(sender=request.user),
            deleted=False)\
        .distinct("distinct_identifier")
    # 获取相关的clubs
    clubs = [x.target_club for x in result if x.chat_type == "group"]
    club_joins = ClubJoining.objects.filter(user=request.user, club__in=clubs)
    users = [x.target_user for x in result if x.chat_type == "private"]
    relation_settings = UserRelationSetting.objects.filter(user=request.user, target__in=users)
    #
    data = dict(
        chats=map(lambda x: x.dict_description(), result),
        club_settings=map(lambda x: x.dict_description(for_host=True, show_members_num=True), club_joins),
        private_settings=map(lambda x: x.dict_description_simple(), relation_settings)
    )
    return JsonResponse(dict(success=True, data=data))


@require_GET
@login_first
def unread_chat_message_num(request):
    """ 统计未读消息数量
    """
    user_result = User.objects.filter(chats__target_user=request.user, chats__read=False).distinct()\
        .annotate(unread_num=Count("chats")).filter(unread_num__gt=0)
    club_result = ClubJoining.objects.filter(user=request.user, unread_chats__gt=0)

    def f(user):
        return dict(user=user.profile.simple_dict_description(), unread=user.unread_num, chat_type="private")

    def g(club):
        return dict(club=club.club.dict_description(), unread=club.unread_chats, chat_type="group")

    user_list = map(f, user_result)
    club_list = map(g, club_result)

    return JsonResponse(dict(success=True, data=(user_list + club_list)))



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
        target_filter = Q(target_user=target_user, sender=request.user) | \
                        Q(target_user=request.user, sender=target_user)
    elif chat_type == "group":
        try:
            # 用户必须是俱乐部的成员才能获取历史信息
            join = ClubJoining.objects.select_related("club").get(club__id=target_id, user=request.user)
            target_club = join.club
            join.chat_sync_date = timezone.now()
            join.save()
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
    )[0:limit]
    if chat_type == "private":
        # group类型下read属性无意义
        ChatRecordBasic.objects.filter(target_filter, chat_type=chat_type, deleted=False).update(read=True)
    return JsonResponse(dict(
            success=True, chats=map(lambda x: x.dict_description(), result)))


@require_POST
@login_first
def read_sync(request):
    """ 同步阅读状态, 将和目标用户/群组的所有对话
    """
    target_id = request.GET["target_id"]
    chat_type = request.GET["chat_type"]

    if chat_type == "private":
        try:
            target_user = User.objects.get(id=target_id)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code="3002", message="User not found"))
        ChatRecordBasic.objects\
            .filter(sender=target_user, read=False, target_user=request.user)\
            .update(read=True)
        return JsonResponse(dict(success=True))
    elif chat_type == "group":
        try:
            target_club = Club.objects.get(id=target_id)
            join = ClubJoining.objects.get(club=target_club, user=request.user)
            join.unread_chats = 0
            join.save()
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code="2002", message="club not found"))
    else:
        return JsonResponse(dict(success=False, code="6002", message="invalid chat type"))


@require_POST
@login_first
def start_chat():
    pass

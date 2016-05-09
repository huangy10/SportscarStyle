# coding=utf-8
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from custom.utils import login_first, page_separator_loader, post_data_loader
from .models import ChatEntity, Chat
from User.models import User
from Club.models import Club, ClubJoining
from .utils import UnreadMessageNumStorage
# Create your views here.


@require_GET
@login_first
def chat_list(request):
    """ 暂时先返回所有的聊天单元
     返回的信息包括每个单元的类型(private/group),目标信息(target_user/target_club),以及最近的一条聊天的内容
    """
    result = ChatEntity.objects.filter(host=request.user)
    return JsonResponse(dict(
        success=True, data=map(lambda x: x.dict_description(), result)
    ))


@require_POST
@login_first
@post_data_loader()
def roster_update(request, data, roster_id):
    try:
        entity = ChatEntity.objects.get(id=roster_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="Roster Item not found"))
    entity.always_on_top = data["always_on_top"]
    entity.no_disturbing = data["no_disturbing"]
    entity.set_nick_name(data["nick_name"])
    return JsonResponse(dict(success=True))


@require_GET
@login_first
def unread_chat_message_num(request):
    """ 统计未读消息数量
    """
    return UnreadMessageNumStorage.get_redis_key(request.user)


@require_GET
@login_first
def historical_record(request):
    """ 获取历史聊天信息
     :param op_type only accept "more"
    """
    roster_id = request.GET["roster"]
    skips = int(request.GET["skips"])
    limit = int(request.GET["limit"])
    try:
        entity = ChatEntity.objects\
            .select_related("user", "club")\
            .get(pk=roster_id, host=request.user)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="Chat entity not found"))
    if entity.user is not None:
        result = Chat.objects.order_by("-created_at").filter(
            Q(sender=entity.user, target_user=entity.host) |
            Q(sender=entity.host, target_user=entity.user)
        )[skips: (skips + limit)]

    elif entity.club is not None:
        club = entity.club.club
        result = Chat.objects.order_by("-created_at").filter(
            target_club=club
        )[skips: (skips + limit)]

    else:
        return JsonResponse(dict(successs=False, message="Internal Error"))

    return JsonResponse(
        dict(success=True, data=map(lambda x: x.dict_description(host=request.user), result))
    )


@login_first
@post_data_loader()
def start_chat(request, data):
    """
     每次进入聊天前需要发送这个请求
    :param request:
    :return:
    """
    chat_type = data["chat_type"]
    target_id = data["target_id"]
    if chat_type == "user":
        try:
            target_user = User.objects.get(pk=target_id)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="User not found"))
        entity, created = ChatEntity.objects.get_or_create(user=target_user, host=request.user)
    elif chat_type == 'club':
        try:
            target_join = ClubJoining.objects.get(club_id=target_id, user=request.user)
            target_club = target_join
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="Club not found"))
        entity, created = ChatEntity.objects.get_or_create(user=target_club, host=request.user)
    else:
        return JsonResponse(dict(success=False, message="Chat type not defined: %s" % chat_type))
    result = entity.dict_description()
    result.update(created=created)
    return JsonResponse(dict(success=True, data=result))


@require_POST
@login_first
def read_sync(request):
    """ 同步阅读状态, 将和目标用户/群组的所有对话
    """
    target_id = request.POST["target_id"]
    chat_type = request.POST["chat_type"]
    cur_unread = request.POST["unread"]
    if chat_type == 'user':
        try:
            target_user = User.objects.get(id=target_id)
            entity = ChatEntity.objects.get(user=target_user, host=request.user)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code="3002", message="User not found"))
        Chat.objects.filter(sender=target_user, read=False, target_user=request.user)\
            .update(read=True)
        entity.unread_num = 0
        entity.save()

        unread = UnreadMessageNumStorage.get_redis_key(request.user)
        if 0 <= cur_unread < unread:
            UnreadMessageNumStorage.set_unread_num(request.user, cur_unread)
        return JsonResponse(dict(success=True))
    elif chat_type == 'club':
        try:
            join = ClubJoining.objects\
                .select_related('club')\
                .get(club_id=target_id, user=request.user)
            entity = ChatEntity.objects.get(club=join.club, host=request.user)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code="2002", message="club not found"))
        join.unread_chats = 0
        join.save()

        entity.unread_num = 0
        unread = UnreadMessageNumStorage.get_redis_key(request.user)
        if 0 <= cur_unread < unread:
            UnreadMessageNumStorage.set_unread_num(request.user, cur_unread)
        return JsonResponse(dict(success=True))




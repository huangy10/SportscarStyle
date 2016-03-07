# coding=utf-8
import json

from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Case, When, Sum, IntegerField

from .forms import ClubCreateForm
from .models import Club, ClubJoining
from custom.utils import post_data_loader, login_first
# Create your views here.


@require_POST
@login_first
def club_create(request):
    """ 创建俱乐部,需要提供初始成员和logo,简介等信息
    """
    users_id = json.loads(request.POST["members"])
    # Manually add host id to POST
    request.POST.update({"host": request.user.id})
    form = ClubCreateForm(request.POST, request.FILES)
    if form.is_valid():
        club = form.save()
        users = []
        try:
            for user_id in users_id:
                users.append(User.objects.select_related("profile").get(id=user_id))
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code=3002, message="User not Found"))
        for user in users:
            ClubJoining.objects.create(club=club, user=user, nick_name=user.profile.nick_name)
        # Also add the host as a member of the club
        ClubJoining.objects.create(user=request.user, club=club, nick_name=request.user.profile.nick_name)
        return JsonResponse(dict(success=True, club=club.dict_description()))
    else:
        print form.errors
        print request.POST
        return JsonResponse(dict(success=False))


@require_GET
@login_first
def club_list(request):
    """ 获取当前用户的所有经过认证的群组
    """
    authed = request.GET.get("authed", "n")
    if authed == "y":
        result = ClubJoining.objects.filter(user=request.user, club__identified=True)
    else:
        result = ClubJoining.objects.filter(user=request.user)
    return JsonResponse(dict(success=True, clubs=map(lambda x: x.dict_description(for_host=True), result)))


@require_GET
@login_first
def club_infos(request, club_id):
    """
    """
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=True, code="2002", message="club not found"))
    try:
        club_join = ClubJoining.objects.get(user=request.user, club=club)
        if request.user == club.host:
            return JsonResponse(
                dict(success=True, data=club_join.dict_description(show_members=True, for_host=True)))
        else:
            return JsonResponse(
                dict(success=True, data=club_join.dict_description(show_members=True, for_host=True)))
    except ObjectDoesNotExist:
        return JsonResponse(success=True, data=club.dict_description(show_members=club.show_members_to_public,
                                                                     show_setting=False))


@require_POST
@login_first
@post_data_loader()
def update_club_settings(request, data, club_id):
    """ 更新俱乐部设置
     如果当前用户是制定俱乐部的创建者,则其可以修改club本身的属性,否则只能修改对应club_join对象
     :param club_id 制定俱乐部的名称

     上传的data中的数据包括:
      _
      |- only_host_can_invite
      |- show_members_to_public
      |- nick_name   我在本群的群昵称
      |- show_nick_name
      |- no_disturbing
      |- always_on_top
      |- logo
      |- name
      |- description
      上述参数不需要全部制定,制定其中任意个均可
    """
    try:
        club_join = ClubJoining.objects.select_related("club").get(club_id=club_id, user=request.user)
        club = club_join.club
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=True, code="2002", message="club not found"))
    new_logo = request.FILES.get("logo", None)
    if new_logo is not None and club.host == request.user:
        club.logo = new_logo
    club_join.update_settings(settings=data, update_club=(club_join.club.host == request.user))
    if new_logo is not None:
        new_logo_url = club.logo.url
        return JsonResponse(dict(success=True, logo=new_logo_url))
    return JsonResponse(dict(success=True))


@require_GET
@login_first
def club_discover(request):
    """ 发现俱乐部
     query_type: nearby/value/members/average/beauty/recent
    """
    query_type = request.GET.get("query_type", "nearby")
    skip = int(request.GET.get("skip", 0))
    limit = int(request.GET.get("limit", 10))
    user = request.user

    if query_type == "nearby":
        city = user.profile.district.split(" ")[0]
        result = Club.objects.filter(city=city, deleted=False)\
            .annotate(members_num=Count("members"))[skip: skip + limit]
    elif query_type == "value":
        result = Club.objects.filter(deleted=False).order_by("-value_total")\
            .annotate(members_num=Count("members"))[skip: skip + limit]
    elif query_type == "members":
        result = Club.objects.filter(deleted=False)\
            .annotate(members_num=Count("members"))\
            .order_by("-members_num")[skip: skip + limit]
    elif query_type == "average":
        result = Club.objects.filter(deleted=False)\
            .annotate(members_num=Count("members"))\
        .order_by("-value_average")[skip: skip + limit]
    elif query_type == "beauty":
        result = Club.objects.filter(deleted=False)\
            .annotate(members_num=Count("members"))\
            .annotate(beauty_num=Sum(
                Case(When(members__profile__gender="f", then=1),
                     default=0, output_field=IntegerField())))\
            .order_by("-beauty_num")[skip: skip + limit]
    elif query_type == "recent":
        result = Club.objects.filter(deleted=False)\
            .annotate(members_num=Count("members"))\
            .order_by("-created_at")[skip: skip + limit]
    else:
        return JsonResponse(dict(success=False))
    return JsonResponse(dict(success=True,
                             data=map(lambda x: x.dict_description(show_value=True, show_members_num=True), result)))
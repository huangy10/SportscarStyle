# coding=utf-8
import json

from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

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
    result = ClubJoining.objects.filter(user=request.user)
    return JsonResponse(dict(success=True, clubs=map(lambda x: x.dict_description(), result)))


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
                dict(success=True, data=club_join.dict_description(show_members=True, for_host=False)))
    except ObjectDoesNotExist:
        return JsonResponse(success=True, data=club.dict_description(show_members=club.show_members_to_public,
                                                                     show_setting=False))

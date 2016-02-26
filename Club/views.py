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
    form = ClubCreateForm(request.POST, request.FILES)
    if form.valid():
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

    else:
        return JsonResponse(dict(success=False))

    return JsonResponse(dict(success=True, clubID=club.id))

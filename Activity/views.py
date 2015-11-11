# coding=utf-8
import json
import datetime

from django.views.decorators.http import require_GET, require_POST
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import Activity, ActivityJoin
from custom.utils import post_data_loader, login_first
from Location.models import Location
from Club.models import Club

# Create your views here.


@require_GET
def activity_discover(request):
    """ 活动发现
    """


@require_GET
def activity_mine(request):
    """ 自己发布的活动
    """


@require_GET
def activity_applied(request):
    """ 自己报名的活动
    """


@require_POST
def activity_apply(request):
    """ 报名活动
    """


@require_POST
@login_first
@post_data_loader()
def activity_create(request, data):
    """ 创建活动
     需要上传的参数为:
      - name
      - description
      - inform_of       提醒的用户的列表
      - max_attend
      - start_at
      - end_at
      - club_limit
      - poster
      - location
       |- lat
       |- lon
       |- description
    """
    if 'inform_of' in data:
        inform_of = json.loads(data['inform_of'])
        users = get_user_model().objects.filter(id__in=inform_of)
    else:
        users = None
    location = json.loads(data['location'])
    if 'club_limit' in data:
        try:
            club_limit = Club.objects.get(id=data['club_limit'])
        except ObjectDoesNotExist:
            club_limit = None
    else:
        club_limit = None
    loc = Location.objects.create(
        location=Point(location['lat'], location['lon']),
        description=location['description'],
    )

    act = Activity.objects.create(
        name=data['name'],
        description=data['description'],
        max_attend=data['max_attend'],
        start_at=timezone.make_aware(datetime.datetime.strptime(data['start_at'], '%Y-%m-%d %H:%M:%S %Z')),
        end_at=timezone.make_aware(datetime.datetime.strptime(data['end_at'], '%Y-%m-%d %H:%M:%S %Z')),
        location=loc,
        allowed_club=club_limit,
        poster=request.FILES['poster'],
    )
    if users is not None:
        act.inform_of.add(*users)
    # TODO: 需要给这些用户发送相应的通知

    return JsonResponse(dict(success=True, act_id=act.id))


@require_POST
def activity_edit(request):
    """ 活动编辑
    """


@require_GET
def activity_detail(request, act_id):
    """ 活动详情, 注意这里只显示活动相关的内容, 评论列表从单独的接口获取
     返回的信息和创建时提交的信息基本一致,但是不用显示inform_of, 回复的club_limit要显示这个俱乐部的标识和id,
     另外要返回报名参加者的列表
    """
    try:
        act = Activity.objects.get(id=act_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='7000', message='Activity not found.'))

    data = dict(
        name=act.name, description=act.description, max_attend=act.max_attend,
        start_at=act.start_at.strftime('%Y-%m-%d %H:%M:%S %Z'),
        end_at=act.end_at.strftime('%Y-%m-%d %H:%M:%S %Z'),
        poster=act.poster.url,
    )

    loc = act.location
    data['location'] = dict(
        lat=loc.location.x, lon=loc.location.y,
        description=loc.description
    )

    apply_list = ActivityJoin.objects.select_related('user__profile__avatar_club').filter(activity=act)
    data['apply_list'] = map(lambda x: dict(approved=x.approved, user=dict(
        id=x.user.id,
        avatar=x.user.profile.avatar.url,

    )), apply_list)




# coding=utf-8
import json
import datetime

from django.views.decorators.http import require_GET, require_POST
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q

from .models import Activity, ActivityJoin, ActivityComment
from custom.utils import post_data_loader, login_first, page_separator_loader
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
        start_at=timezone.make_aware(datetime.datetime.strptime(data['start_at'], '%Y-%m-%d %H:%M:%S')),
        end_at=timezone.make_aware(datetime.datetime.strptime(data['end_at'], '%Y-%m-%d %H:%M:%S')),
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
@login_first
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
        start_at=act.start_at.strftime('%Y-%m-%d %H:%M:%S'),
        end_at=act.end_at.strftime('%Y-%m-%d %H:%M:%S'),
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
        avatar_car=x.user.profile.avatar_car.logo if x.user.profile.avatar_car is not None else None
    )), apply_list)

    return JsonResponse(dict(success=True, data=data))


@require_GET
@login_first
@page_separator_loader
def activity_detail_comment(request, date_threshold, op_type, limit, act_id):
    """ 获取活动下方的评论
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    comments = ActivityComment.objects.filter(date_filter, activity_id=act_id).\
        values('user__profile__nick_name', 'user__id', 'created_at', 'image', 'response_to__id', 'id')[0: limit]

    def format_fix(comment):
        comment['user_id'] = comment['user__id']
        comment['user_nickname'] = comment['user__profile__nick_name']
        comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        del comment['user__id']
        del comment['user__profile__nick_name']
        return comment
    comments = map(format_fix, comments)
    return JsonResponse(dict(
        success=True,
        comments=list(comments)
    ))


@require_POST
@login_first
@post_data_loader(json_fields=('inform_of', ))
def post_activity_comment(request, data, act_id):
    """ 对活动发布评论
     返回分配给这个活动的id
    """
    try:
        activity = Activity.objects.get(id=act_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="Activity not found", code='7000'))

    if 'response_to' in data:
        try:
            response_to = ActivityComment.objects.get(id=data['response_to'])
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code='7001', message='Activity comment not found.'))
    else:
        response_to = None

    try:
        comment = ActivityComment.objects.create(
            user=request.user, image=request.FILES.get('image', None),
            content=data.get('content', None), response_to=response_to, activity=activity
        )
    except ValidationError:
        return JsonResponse(dict(success=False, code='7002', message='No valid content found for the comment'))

    if 'inform_of' in data:
        inform_users = get_user_model().objects.filter(id__in=data['json_data'])
        comment.inform_of.add(*inform_users)

    return JsonResponse(dict(success=True, id=comment.id))

# coding=utf-8
import json
import datetime

from django.views.decorators.http import require_GET, require_POST
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q, Count

from .models import Activity, ActivityJoin, ActivityComment
from custom.utils import post_data_loader, login_first, page_separator_loader
from Location.models import Location
from Club.models import Club

# Create your views here.


@require_GET
def activity_discover(request):
    """ 活动发现,需要提交的参数是query的范围,包括:用户所在位置经纬度,query的distance
    """
    # 获取用户的坐标
    lat = float(request.GET.get("lat"))
    lon = float(request.GET.get("lon"))
    user_position = Point(lon, lat)
    # 检索的距离,单位为km
    query_distance = float(request.GET.get("query_distance", 10.0))
    #
    limit = int(request.GET.get("limit"))
    skip = int(request.GET.get("skip"))
    #
    acts = Activity.objects\
        .annotate(comment_num=Count('comments')).annotate(like_num=Count("liked_by"))\
        .filter(location__location__distance_lte=(user_position, D(km=query_distance)))[skip: skip + limit]

    return JsonResponse(dict(success=True,
                             acts=map(lambda x: x.dict_description_with_aggregation(with_user_info=True), acts)))


@require_GET
@page_separator_loader
def activity_mine(request, date_threshold, op_type, limit):
    """ 自己发布的活动
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    acts = Activity.objects.select_related("allowed_club")\
        .annotate(comment_num=Count('comments')).annotate(like_num=Count("liked_by"))\
        .filter(date_filter, user=request.user).order_by("-created_at")[0: limit]

    return JsonResponse(dict(success=True, acts=map(lambda x: x.dict_description_with_aggregation(with_user_info=True), acts)))


@require_GET
@login_first
@page_separator_loader
def activity_applied(request, date_threshold, op_type, limit):
    """ 自己报名的活动
    """

    if op_type == 'latest':
        date_filter = Q(applications__created_at__gt=date_threshold)
    else:
        date_filter = Q(applications__created_at__lt=date_threshold)
    #  统计评论数量和点赞数量
    result = Activity.objects.select_related("user__profile")\
        .annotate(comment_num=Count('comments')).annotate(like_num=Count("liked_by"))\
        .order_by("applications__created_at").filter(date_filter, applications__user=request.user)[0:limit]
    return JsonResponse(dict(success=True, acts=map(lambda x: x.dict_description_with_aggregation(with_user_info=True), result)))


@require_POST
@login_first
def activity_apply(request, act_id):
    """ 报名活动
    """
    try:
        act = Activity.objects.get(id=act_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code="7001", message="Activity with id %s not found" % act_id))

    join, created = ActivityJoin.objects.get_or_create(user=request.user, activity=act)
    if not created:
        join.approved = False
        join.save()
        # join字段表明最终操作是报名还是取消报名
        return JsonResponse(dict(success=True, join=False))
    return JsonResponse(dict(success=True, join=True))


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
    print(data)
    print(request.POST)
    print(request.FILES)
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
        location=Point(location['lon'], location['lat']),
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
        user=request.user
    )
    if users is not None:
        act.inform_of.add(*users)
    # TODO: 需要给这些用户发送相应的通知

    return JsonResponse(dict(success=True, id=act.id))


@require_POST
def activity_edit(request):
    """ 活动编辑
    """


def activity_close(request, act_id):
    """ 关闭活动报名
    """
    try:
        act = Activity.objects.get(id=act_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code="7001", message="Activity with id %s not found" % act_id))
    act.closed = True
    act.closed_at = timezone.now()
    act.save()
    return JsonResponse(dict(success=True))



@require_GET
@login_first
def activity_detail(request, act_id):
    """ 活动详情, 注意这里只显示活动相关的内容, 评论列表从单独的接口获取
     返回的信息和创建时提交的信息基本一致,但是不用显示inform_of, 回复的club_limit要显示这个俱乐部的标识和id,
     另外要返回报名参加者的列表
    """
    try:
        act = Activity.objects.annotate(comment_num=Count('comments')).annotate(like_num=Count("liked_by"))\
            .get(id=act_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='7000', message='Activity not found.'))

    data = act.dict_description_with_aggregation(with_user_info=True)
    print(data)
    apply_list = ActivityJoin.objects.select_related('user__profile__avatar_club').filter(activity=act)
    data['apply_list'] = map(lambda x: dict(approved=x.approved,
                                            like_at=x.created_at.strftime('%Y-%m-%d %H:%M:%S %Z'),
                                            user=x.user.profile.complete_dict_description()),
                             apply_list)

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

    comments = ActivityComment.objects\
        .select_related("user__profile")\
        .filter(date_filter, activity_id=act_id)[0:limit]

    comments = map(lambda x: x.dict_description_simple(), comments)
    return JsonResponse(dict(
        success=True,
        comments=comments
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

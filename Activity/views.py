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

from User.models import User
from custom.views import LoginFirstOperationView
from .models import Activity, ActivityJoin, ActivityComment
from custom.utils import post_data_loader, login_first, page_separator_loader, time_to_string, get_logger
from Location.models import Location
from Club.models import Club, ClubJoining
from Notification.signal import send_notification
from Notification.models import Notification
from Sportscar.models import SportCarOwnership

# Create your views here.


logger = get_logger(__name__)


@require_GET
def activity_discover(request):
    """ 活动发现,需要提交的参数是query的范围,包括:用户所在位置经纬度,query的distance
    """
    # 获取用户的坐标
    lat = float(request.GET.get("lat"))
    lon = float(request.GET.get("lon"))
    city_limit = request.GET.get("city_limit", u"全国")
    if city_limit != u"全国":
        city_filter_q = Q(location__city__startswith=city_limit)
    else:
        city_filter_q = None

    user_position = Point(lon, lat)
    # 检索的距离,单位为km
    query_distance = float(request.GET.get("query_distance", 10.0))
    #
    limit = int(request.GET.get("limit"))
    skip = int(request.GET.get("skip"))
    #

    if city_filter_q is None:
        acts = Activity.objects\
            .filter(location__location__distance_lte=(user_position, D(km=query_distance)),
                    closed=False, end_at__gt=timezone.now(), allowed_club=None)\
            .distinct()[skip: (skip + limit)]
    else:
        acts = Activity.objects.filter(city_filter_q, closed=False, end_at__gt=timezone.now(), allowed_club=None)\
            .distinct()[skip: (skip + limit)]

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
        .filter(date_filter, user=request.user).order_by("-created_at")[0: limit]

    return JsonResponse(dict(success=True, \
        acts=map(lambda x: x.dict_description_with_aggregation(with_user_info=True), acts)))


@require_GET
@login_first
@page_separator_loader
def activity_applied(request, date_threshold, op_type, limit):
    """ 自己报名的活动
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)
    #  统计评论数量和点赞数量
    result = ActivityJoin.objects\
        .select_related("activity")\
        .filter(date_filter, user=request.user, approved=True)[0: limit]
    return JsonResponse(dict(success=True,
        acts=map(lambda x: x.dict_description(), result)))


@require_POST
@login_first
def activity_apply(request, act_id):
    """ 报名活动
    """
    try:
        act = Activity.objects.get(id=act_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code="7001", message="Activity with id %s not found" % act_id))
    # permission check
    if act.authed_user_only and not request.user.identified:
        return JsonResponse(dict(success=False, message="no permission"))

    # club = act.allowed_club
    # if club is not None:
    #     if not ClubJoining.objects.filter(club=club, user=request.user).exists():
    #         logger.debug(u'有个用户试图加入一个他并未加入的俱乐部的活动,权限问题。用户为{phone}, 活动为{act_id}'.format(
    #             phone=request.user.username, act_id=act_id
    #         ))
    #         return JsonResponse(dict(success=False, message='Not Allowed'))

    # 检查是否已经报满了

    current_join_count = ActivityJoin.objects.filter(activity=act, approved=True).count()
    if current_join_count >= act.max_attend:
        return JsonResponse(dict(success=False, message="full"))

    join, created = ActivityJoin.objects.get_or_create(user=request.user, activity=act)

    if not created:
        logger.debug(u'对活动{act_id}出现了重复报名, 用户为{phone}'.format(act_id=act_id, phone=request.user.username))
        return JsonResponse(dict(success=False, message="denied"))
    else:
        # send a notification to the host of the activity
        # send_notification.send(sender=Activity,
        #                        target=act.user,
        #                        related_user=request.user,
        #                        message_type="act_applied",
        #                        related_act=act,
        #                        message_body="")
        send_notification.send(
            sender=ActivityJoin,
            target=act.user,
            display_mode="interact",
            extra_info="apply",
            related_user=request.user,
            related_act=act
        )
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
       |- city
    """
    if not SportCarOwnership.objects.filter(user=request.user, identified=True).exists():
        return JsonResponse(dict(success=False, message="no permission"))
    if 'inform_of' in data:
        inform_of = json.loads(data['inform_of'])
        users = get_user_model().objects.filter(id__in=inform_of)
    else:
        users = None
    location = json.loads(data['location'])
    # if 'club_limit' in data:
    #     try:
    #         club_limit = Club.objects.get(id=data['club_limit'])
    #     except ObjectDoesNotExist:
    #         club_limit = None
    # else:
    #     club_limit = None
    loc = Location.objects.create(
        location=Point(location['lon'], location['lat']),
        description=location['description'],
        city=location.get("city") or ""
    )
    print location
    act = Activity.objects.create(
        name=data['name'],
        description=data['description'],
        max_attend=data['max_attend'],
        start_at=datetime.datetime.strptime(data['start_at'], '%Y-%m-%d %H:%M:%S.%f %Z'),
        end_at=datetime.datetime.strptime(data['end_at'], '%Y-%m-%d %H:%M:%S.%f %Z'),
        location=loc,
        allowed_club=None,
        poster=request.FILES['poster'],
        user=request.user,
        authed_user_only=data["authed_user_only"]
    )
    # ActivityJoin.objects.create(user=request.user, activity=act)
    if users is not None:
        act.inform_of.add(*users)
        for user in users:
            # send_notification.send(
            #     sender=Activity,
            #     target=user,
            #     related_act=act,
            #     related_user=request.user,
            #     message_type="act_invited",
            #     message_body=""
            # )
            send_notification.send(
                sender=ActivityJoin,
                target=user,
                display_mode="interact",
                extra_info="invited",
                related_act=act,
                related_user=request.user
            )

    return JsonResponse(dict(success=True, id=act.id))


@require_POST
@login_first
def activity_edit(request, act_id):
    """ 活动编辑
    """
    try:
        act = Activity.objects.get(id=act_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="act not found"))
    data = request.POST
    if act.user != request.user:
        return JsonResponse(dict(success=False, message="no permission"))
    act.name = data['name']
    act.description = data['description']
    act.user = request.user
    act.max_attend = data["max_attend"]
    act.start_at = datetime.datetime.strptime(data['start_at'], '%Y-%m-%d %H:%M:%S.%f %Z')
    act.end_at = datetime.datetime.strptime(data['end_at'], '%Y-%m-%d %H:%M:%S.%f %Z')
    act.poster = request.FILES['poster']
    act.authed_user_only = data["authed_user_only"]
    location = json.loads(data['location'])
    loc, _ = Location.objects.get_or_create(
        location=Point(location['lon'], location['lat']),
        description=location['description'],
    )
    act.location = loc
    if 'inform_of' in data:
        inform_of = json.loads(data["inform"])
        users = User.objects.filter(id__in=inform_of)
        if not users.count() == len(inform_of):
            return JsonResponse(dict(success=False, message="Invalid data"))
        act.inform_of.add(*users)

    act.save()
    return JsonResponse(dict(success=True, data=act.dict_description_with_aggregation(with_user_info=True)))


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


class ActivityOperation(LoginFirstOperationView):

    operations = ["kick_out", "invite", "invite_agree", "invite_deny", "like", "act_remove_member"]

    def kick_out(self, request, data, act_id):
        # TODO: 去掉活动申请加入的审核,直接加进来就可以了
        applier = data.get("target_user")
        try:
            join = ActivityJoin.objects.select_related("user", "activity").get(user_id=applier, activity_id=act_id)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="Application not found"))
        # send_notification.send(
        #     sender=ActivityJoin,
        #     target=join.user,
        #     related_act=join.activity,
        #     message_type="kickout",
        #     message_body=""
        # )
        join.delete()
        send_notification.send(
            sender=ActivityJoin,
            target=join.user,
            display_mode="with_cover",
            extra_info="kick_out",
            related_act=join.activity,
            related_user=request.user
        )
        return JsonResponse(dict(success=True))

    def invite(self, request, data, act_id):
        appliers = data.get('target_user')
        appliers = json.loads(appliers)
        try:
            act = Activity.objects.get(id=act_id)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=True, message="Activity Not Found"))
        users = User.objects.filter(~Q(id=request.user.id), id__in=appliers)
        if len(users) != len(appliers):
            return JsonResponse(dict(success=False, message="user id list is not valid"))
        for user in users:
            # send_notification.send(
            #     sender=ActivityJoin,
            #     target=user,
            #     related_user=request.user,
            #     related_act=act,
            #     message_type="act_invited",
            #     message_body=""
            # )
            send_notification.send(
                sender=ActivityJoin,
                target=user,
                display_mode="interact",
                extra_info="invited",
                related_act=act,
                related_user=request.user
            )
        return JsonResponse(dict(success=True))

    def invite_agree(self, request, data, act_id):
        inviter_id = data.get('target_user')
        try:
            notif = Notification.objects.select_related("related_act").get(
                extra_info="invited",
                sender_class_name=ActivityJoin.__name__,
                target=request.user,
                related_act_id=act_id,
                related_user_id=inviter_id,
                checked=False
            )
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="Not Invited"))
        # 检查是否已经报满了
        act = notif.related_act
        cur_join_num = ActivityJoin.objects.filter(activity=act, approved=True).count()
        if cur_join_num >= act.max_attend:
            return JsonResponse(dict(success=False, message="full"))
        notif.flag = True
        notif.checked = True
        notif.save()
        # send_notification.send(
        #     sender=Activity,
        #     target=notif.related_user,
        #     related_user=request.user,
        #     related_act=notif.related_act,
        #     message_type="act_invitation_agreed",
        #     message_body=""
        # )
        send_notification.send(
            sender=ActivityJoin,
            target=notif.related_user,
            display_mode="minimal",
            extra_info="invite_agreed",
            related_user=request.user,
            related_act=notif.related_act
        )
        join, created = ActivityJoin.objects.get_or_create(
            user=request.user, activity=act
        )
        if not created:
            join.approved = True
            join.save()

        return JsonResponse(dict(success=True))

    def invite_deny(self, request, data, act_id):
        applier = data.get('target_user')
        try:
            notif = Notification.objects.select_related("related_act", "related_user").get(
                extra_info="invited",
                sender_class_name=ActivityJoin.__name__,
                target=request.user,
                related_user_id=applier,
                related_act_id=act_id,
                checked=False
            )
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="Not invited"))

        notif.flag = False
        notif.checked = True
        notif.save()
        #
        # send_notification.send(
        #     sender=Activity,
        #     target=notif.related_user,
        #     related_act=notif.related_act,
        #     related_user=request.user,
        #     message_type="act_invitation_denied",
        #     message_body=""
        # )
        send_notification.send(
            sender=ActivityJoin,
            target=notif.related_user,
            display_mode="minimal",
            extra_info="invite_denied",
            related_user=request.user,
            related_act=notif.related_act
        )
        join, created = ActivityJoin.objects.get_or_create(
            user=request.user, activity=notif.related_act
        )
        if created and join.approved:
            join.approved = False
            join.save()
        return JsonResponse(dict(success=True))

    def like(self, request, data, act_id):
        try:
            act = Activity.objects.get(id=act_id)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="activity not found"))
        if act.liked_by.filter(id=request.user.id).exists():
            act.liked_by.remove(request.user)
            act.like_num -= 1
            act.save()
            return JsonResponse(dict(success=True, data=dict(liked=False, like_num=act.liked_by.count())))
        else:
            act.like_num += 1
            act.liked_by.add(request.user)
            act.save()
            send_notification.send(
                sender=Activity,
                target=act.user,
                display_mode="minimal",
                extra_info="like",
                related_act=act,
                related_user=request.user
            )
            return JsonResponse(dict(success=True, data=dict(liked=True, like_num=act.liked_by.count())))

    def act_remove_member(self, request, data, act_id):
        applier = data.get('target_user')
        try:
            join = ActivityJoin.objects.select_related("activity")\
                .get(user=applier, activity_id=act_id, approved=True)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="Not Joined"))
        join.approved = False
        join.save()
        return JsonResponse(dict(success=True))


#
# @require_POST
# @login_first
# @post_data_loader()
# def activity_operation(request, data, act_id):
#     """ 对活动的操作,目前支持:
#      - 批准活动申请
#      - 邀请他人
#     """
#     op_type = data.get("op_type")
#     if op_type == "apply_deny":
#         applier = data.get("target_user")
#         try:
#             join = ActivityJoin.objects.get(user_id=applier, activity_id=act_id)
#         except ObjectDoesNotExist:
#             return JsonResponse(dict(success=False, message="Application not found"))
#         join.approved = False
#         join.save()
#         # send a notification to the guy who applied the activity
#         send_notification.send(sender=ActivityJoin,
#                                target=join.user,
#                                related_act=join.activity,
#                                message_type="act_denied",
#                                message_body="")
#         return JsonResponse(dict(success=True))
#     elif op_type == "invite":
#         # invite users to
#         appliers = data.get("target_user")
#         appliers = json.loads(appliers)
#         try:
#             act = Activity.objects.get(id=act_id)
#         except ObjectDoesNotExist:
#             return JsonResponse(dict(success=True, message="Activity Not found"))
#         users = get_user_model().objects.filter(~Q(id=request.user.id), id__in=appliers)
#         if len(users) != len(appliers):
#             return JsonResponse(dict(success=False, message="user id list is not valid"))
#         for user in users:
#             send_notification.send(sender=ActivityJoin,
#                                    target=user,
#                                    related_user=request.user,
#                                    related_act=act,
#                                    message_type="act_invited",
#                                    message_body="")
#         return JsonResponse(dict(success=True))
#     elif op_type == "invite_accepted":
#         # applier = data.get("target_user")
#         try:
#             notif = Notification.objects.get(message_type="act_invited",
#                                              target=request.user,
#                                              related_act__id=act_id, checked=False)
#         except ObjectDoesNotExist:
#             return JsonResponse(dict(success=False, message="Not invited"))
#         # 检查活动是否已经报满了
#         act = notif.related_act
#         cur_join_num = ActivityJoin.objects.filter(activity=act, approved=True).count()
#         if cur_join_num >= act.max_attend:
#             return JsonResponse(dict(success=False, message="full"))
#         notif.flag = True
#         notif.checked = True
#         notif.save()
#         send_notification.send(
#             sender=Activity,
#             target=notif.related_user,
#             related_user=request.user,
#             related_act=notif.related_act,
#             message_type="act_invitation_agreed",
#             message_body=""
#         )
#         ActivityJoin.objects.create(user=request.user, activity=notif.related_act,
#                                     approved=True)
#         return JsonResponse(dict(success=True))
#     elif op_type == "invite_denied":
#         applier = data.get("target_user")
#         try:
#             notif = Notification.objects.get(message_type="act_invited",
#                                              target=request.user,
#                                              related_user_id=applier,
#                                              related_act__id=act_id, flag=False)
#         except ObjectDoesNotExist:
#             return JsonResponse(dict(success=False, message="Not invited"))
#         notif.flag = False
#         notif.checked = True
#         notif.save()
#         send_notification.send(
#             sender=Activity,
#             target=notif.related_user,
#             related_user=request.user,
#             related_act=notif.related_act,
#             message_type="act_invitation_denied",
#             message_body=""
#         )
#         ActivityJoin.objects.create(user=request.user, activity=notif.related_act,
#                                     approve=False)
#         return JsonResponse(dict(success=True))
#     elif op_type == "like":
#         try:
#             act = Activity.objects.get(id=act_id)
#         except ObjectDoesNotExist:
#             return JsonResponse(dict(success=False, message="activity not found"))
#         if act.liked_by.filter(id=request.user.id).exists():
#             act.liked_by.remove(request.user)
#             act.like_num -= 1
#             act.save()
#             return JsonResponse(dict(success=True, data=dict(liked=False, like_num=act.liked_by.count())))
#         else:
#             act.like_num += 1
#             act.liked_by.add(request.user)
#             act.save()
#             return JsonResponse(dict(success=True, data=dict(liked=True, like_num=act.liked_by.count())))
#     return JsonResponse(dict(success=False, message="Undefined operation type"))


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

    data = act.dict_description_with_aggregation(with_user_info=True)
    apply_list = ActivityJoin.objects.select_related('user__avatar_club').filter(activity=act, approved=True)
    data['apply_list'] = map(lambda x: dict(approved=x.approved,
                                            like_at=time_to_string(x.created_at),
                                            user=x.user.dict_description()),
                             apply_list)
    data["liked"] = act.liked_by.filter(id=request.user.id).exists()
    data["applied"] = ActivityJoin.objects.filter(user=request.user, activity=act, approved=True).exists()
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
        .select_related("user")\
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

    return JsonResponse(
        dict(success=True,
             data=dict(id=comment.id, comment_num=ActivityComment.objects.filter(activity=activity).count()))
    )

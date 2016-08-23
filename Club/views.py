# coding=utf-8
import json

from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Case, When, Sum, IntegerField, BooleanField, Value, Q

from Chat.ChatServer.interface import send_string_message
from Notification.models import Notification
from .forms import ClubCreateForm
from .models import Club, ClubJoining, ClubAuthRequest
from User.models import User
from custom.utils import post_data_loader, login_first, get_logger
from Activity.models import Activity
from Notification.signal import send_notification
from Chat.models import ChatEntity
from Club.models import ClubBillboard

from custom.views import LoginFirstOperationView

# Create your views here.


logger = get_logger(__name__)
CLUB_MEMBERS_DISPLAY_NUM = 12   # 3行,每行4个


@cache_page(60 * 60 * 24)
def club_popular_cities(request):
    result = Club.objects.values("city").annotate(city_num=Count("city"))\
        .order_by("-city_num")\
        .values_list("city", flat=True)[0:9]
    return JsonResponse(dict(success=True, data=list(result)))


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
                users.append(User.objects.get(id=user_id))
        except ObjectDoesNotExist:
            logger.error(u'创建活动时初始化成员失败,成员信息为%s' % users_id)
            return JsonResponse(dict(success=False, code=3002, message="User not Found"))
        for user in users:
            ClubJoining.objects.create(club=club, user=user, nick_name=user.nick_name)
        # Also add the host as a member of the club

        ClubJoining.objects.create(user=request.user, club=club, nick_name=request.user.nick_name)
        entity, _ = ChatEntity.objects.get_or_create(host=request.user, club=club)
        # try:90
        #     ChatRecordBasic.objects.create(target_club=club, chat_type="group", message_type="placeholder",
        #                                sender=request.user)
        # except Exception, e:
        #     print e
        result = club.dict_description(show_members_num=True)
        result.update(roster=entity.dict_description())
        return JsonResponse(dict(success=True, club=result))
    else:
        logger.error(u'创建活动失败,错误信息为%s' % form.errors)
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
        return JsonResponse(dict(success=False, code="2002", message="club not found"))
    try:
        club_join = ClubJoining.objects.get(user=request.user, club=club)
        response_data = club_join.dict_description(show_members=True, for_host=True)
        recent_act = Activity.objects.filter(allowed_club=club).first()
        if recent_act is not None:
            response_data.update(recent_act=recent_act.dict_description_with_aggregation(with_user_info=True))
        return JsonResponse(
            dict(success=True, data=response_data))
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=True, data=club.dict_description(show_members=club.show_members_to_public,
                                                                     show_setting=False)))


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
        return JsonResponse(dict(success=False, code="2002", message="club not found"))
    new_logo = request.FILES.get("logo", None)
    if new_logo is not None and club.host == request.user:
        club.logo = new_logo
    print data
    club_join.update_settings(settings=data, update_club=(club_join.club.host == request.user))
    if new_logo is not None:
        new_logo_url = club.logo.url
        return JsonResponse(dict(success=True, logo=new_logo_url))
    else:
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

    result = Club.objects.filter(deleted=False).annotate(members_num=Count("members"))\
        .annotate(
            attended_count=Sum(
                Case(When(members=request.user, then=Value(1)), default=Value(0), output_field=IntegerField())
            ))
    city_limit = request.GET.get("city_limit", u"全国")
    if city_limit != u'全国':
        result = result.filter(city__startswith=city_limit)

    if query_type == "nearby":
        city = user.district.split(u'市')[0]
        result = result.filter(city__startswith=city)
    elif query_type == "value":
        result = result.order_by("-value_total")
    elif query_type == "members":
        result = result.order_by("-members_num")
    elif query_type == "average":
        result = result.order_by("-value_average")
    elif query_type == "beauty":
        result = result.annotate(
            beauty_num=Sum(
                Case(When(members__gender="f", then=1),
                     default=0, output_field=IntegerField())
            )).order_by("-beauty_num")
    elif query_type == "recent":
        result.order_by("-created_at")
    else:
        return JsonResponse(dict(success=False))

    # if query_type == "nearby":
    #     city = user.district.split(" ")[0]
    #     result = Club.objects.filter(city=city, deleted=False)\
    #         .annotate(members_num=Count("members"))\
    #         .annotate(
    #         attended_count=Sum(
    #             Case(When(members=request.user, then=Value(1)), default=Value(0), output_field=IntegerField())
    #         )
    #     )
    # elif query_type == "value":
    #     result = Club.objects.filter(deleted=False).order_by("-value_total")\
    #         .annotate(members_num=Count("members")) \
    #         .annotate(
    #         attended_count=Sum(
    #             Case(When(members=request.user, then=Value(1)), default=Value(0), output_field=IntegerField())
    #         )
    #     )
    # elif query_type == "members":
    #     result = Club.objects.filter(deleted=False)\
    #         .annotate(members_num=Count("members")) \
    #         .order_by("-members_num")
    #
    # elif query_type == "average":
    #     result = Club.objects.filter(deleted=False)\
    #         .annotate(members_num=Count("members"))\
    #         .annotate(attended=Case(When(members=request.user, then=True), default=False, output_field=BooleanField()))\
    #         .order_by("-value_average")
    # elif query_type == "beauty":
    #     result = Club.objects.filter(deleted=False)\
    #         .annotate(members_num=Count("members"))\
    #         .annotate(beauty_num=Sum(
    #             Case(When(members__gender="f", then=1),
    #                  default=0, output_field=IntegerField())))\
    #         .order_by("-beauty_num")
    # elif query_type == "recent":
    #     result = Club.objects.filter(deleted=False) \
    #         .annotate(members_num=Count("members")) \
    #         .order_by("-created_at")
    # else:
    #     return JsonResponse(dict(success=False))

    # city_limit = request.GET.get("city_limit")
    # if city_limit is not None and city_limit != u"全国":
    #     result = result.filter(city=city_limit)

    result = result[skip: skip + limit]

    for temp in result:
        setattr(temp, "attended", temp.attended_count > 0)

    return JsonResponse(
        dict(success=True,
             data=map(lambda x: x.dict_description(show_value=True, show_members_num=True, show_attended=True),
                      result)))


@login_first
@post_data_loader(force_json=True)
def club_member_change(request, data, club_id):
    """ 俱乐部成员变更
    """
    def post():
        op_type = data.get("op_type")
        target_list = data.get("target_users")

        try:
            club = Club.objects.get(id=club_id)
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="club not exists"))
        # Check the permisson
        if club.only_host_can_invite and club.host != request.user:
            logger.warning(u'俱乐部{club_id}只有群主才能加入新成员,现在有用户{phone}试图加入其它成员'.format(
                club_id=club_id, phone=request.user.username
            ))
            return JsonResponse(dict(success=False, message="no permisson"))
        if op_type == "delete":
            if club.host != request.user:
                logger.warning(u'只有群主才能执行踢出成员的操作,现在的操作者是{phone}, 涉及俱乐部是{club_id}'.format(
                    phone=request.user.username, club_id=club_id
                ))
                return JsonResponse(dict(success=False, message="no permisson"))
            joins = ClubJoining.objects.filter(user__in=target_list, club_id=club_id)
            if joins.count() != len(target_list):
                logger.warning(u'删除群({club_id})成员时,数据一致性出现问题'.format(club_id=club_id))
                return JsonResponse(dict(success=False, message="Invalid user data"))
            joins.delete()
            entities = ChatEntity.objects.filter(club=club, host__in=target_list)
            entities.delete()
            return JsonResponse(dict(success=True))
        elif op_type == "add":
            users = User.objects.filter(id__in=target_list)
            if users.count() != len(target_list):
                return JsonResponse(dict(success=False, message="Invalid user data"))
            ClubJoining.objects.bulk_create(
                [ClubJoining(user=user, club=club) for user in users]
            )
            return JsonResponse(dict(success=True))
        else:
            return JsonResponse(dict(success=False, message="Undefined operation type"))

    def get():
        try:
            club = Club.objects.get(id=club_id)
        except ObjectDoesNotExist:
            return JsonResponse(success=False, message=u"Club not found")
        skip = request.GET.get("skip", 0)
        limit = request.GET.get("limit", 10)

        filter_str = request.GET.get("filter", "")
        if filter_str != "":
            filter_elements = filter_str.split(" ")
            filter_q = Q()
            for filter_element in filter_elements:
                filter_q = filter_q | Q(user__nick_name__icontains=filter_element)
        else:
            filter_q = Q()

        # joins = ClubJoining.objects.filter(filter_q, club=club)[skip: (skip + limit)]
        # payload = map(lambda x: x.dict_description(), joins)
        # members = club.members.filter(filter_q)[skip: (skip + limit)]
        # payload = map(lambda x: x.dict_description(), members)
        members = ClubJoining.objects.select_related("user").filter(filter_q, club=club)[skip: (skip + limit)]

        def member_data_builder(u):
            temp = u.user.dict_discription()
            temp.update(club_name=temp.nick_name)

        payload = map(member_data_builder, members)
        return JsonResponse(dict(success=True, members=payload))

    if request.method == "GET":
        return get()
    else:
        return post()


@require_POST
@login_first
@post_data_loader()
def club_auth(request, data, club_id):
    city = data.get("city")
    des = data.get("description")
    try:
        club = Club.objects.get(id=club_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="Club not found"))
    if club.host != request.user:
        logger.debug(u'只有群主才能发起俱乐部认证,当前操作用户是{phone}, 涉及俱乐部是{club_id}'.format(
            phone=request.user.username, club_id=club_id
        ))
        return JsonResponse(dict(success=False, message="No permission"))

    auth, created = ClubAuthRequest.objects.get_or_create(club=club)
    if not created and not auth.approve and auth.checked:
        logger.debug(u'申请(%s->%s)已经被驳回' % (request.user.username, club_id))
        return JsonResponse(dict(success=False, message="Already Denied"))

    if not created and auth.approve:
        logger.debug(u'申请(%s->%s)已经批准' % (request.user.username, club_id))
        return JsonResponse(dict(success=False, message="Already Identified"))

    auth.city = city
    auth.description = des
    auth.save()

    return JsonResponse(dict(success=True))


@require_POST
@login_first
@post_data_loader()
def club_quit(request, data, club_id):
    print data
    try:
        join = ClubJoining.objects.select_related("club").get(club_id=club_id, user=request.user)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="Not joined"))
    club = join.club

    if join.user == club.host:
        new_host = data["new_host"]
        try:
            new_host = ClubJoining.objects.get(club_id=club_id, user_id=new_host)
            if new_host == join:
                return JsonResponse(dict(success=False, message="Invalid data"))
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="User not Found"))
        club.host = new_host.user
        club.save()
    join.delete()
    return JsonResponse(dict(success=True))


@require_POST
@login_first
def club_apply(request, club_id):
    try:
        club = Club.objects.get(pk=club_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="club not found"))
    if ClubJoining.objects.filter(user=request.user, club=club).exists():
        return JsonResponse(dict(success=False, message="already join"))
    if Notification.objects.filter(
        target=club.host,
        related_user=request.user,
        related_club=club,
        sender_class_name=ClubJoining.__name__,
        extra_info="apply",
        checked=False,
    ).exists():
        return JsonResponse(dict(success=False, message="already applied"))
    # send_notification.send(
    #     sender=Club,
    #     target=club.host,
    #     related_user=request.user,
    #     related_club=club,
    #     message_type="club_apply",
    #     message_body=""
    # )
    send_notification.send(
        sender=ClubJoining,
        target=club.host,
        display_mode="interact",
        extra_info="apply",
        related_club=club,
        related_user=request.user
    )
    return JsonResponse(dict(success=True))


@require_POST
@login_first
@post_data_loader()
def club_operation(request, data, club_id):
    op_type = data.get("op_type")
    if op_type == "club_apply_agree":
        applier = data.get("target_user")
        try:
            notif = Notification.objects\
                .select_related("related_club", "related_user", "target")\
                .get(
                    extra_info="apply",
                    sender_class_name=ClubJoining.__name__,
                    related_user_id=applier,
                    target=request.user,
                    related_club_id=club_id,
                )
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="Applicant not found"))
        notif.checked = True
        notif.flag = True
        notif.save()
        # send_notification.send(
        #     sender=Club,
        #     target=notif.related_user,
        #     related_user=notif.target,
        #     related_club=notif.related_club,
        #     message_type="club_apply_agreed",
        #     message_body=""
        # )
        send_notification.send(
            sender=ClubJoining,
            target=notif.related_user,
            display_mode="with_cover",
            extra_info="agree",
            related_user=notif.target,
            related_club=notif.related_club
        )
        ClubJoining.objects.get_or_create(
            user=notif.related_user,
            club=notif.related_club
        )
        # create the related chat entity
        entity, created = ChatEntity.objects.get_or_create(
            host=notif.related_user,
            club=notif.related_club
        )
        if created:
            message = entity.dict_description()
            message = json.dumps({"target_user": entity.host.id, "payload": message})
            send_string_message(message)
        return JsonResponse(dict(success=True))
    elif op_type == "club_apply_denied":
        applier = data.get("target_user")
        try:
            notif = Notification.objects \
                .select_related("related_club", "related_user", "target") \
                .get(
                    extra_info="apply",
                    sender_class_name=ClubJoining.__name__,
                    related_user_id=applier,
                    target=request.user,
                    related_club_id=club_id,
                )
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message="Applicant not found"))
        notif.checked = True
        notif.flag = False
        notif.save()
        # send_notification.send(
        #     sender=Club,
        #     target=notif.related_user,
        #     related_user=notif.target,
        #     related_club=notif.related_club,
        #     message_type="club_apply_denied",
        #     message_body=""
        # )
        send_notification.send(
            sender=ClubJoining,
            target=notif.related_user,
            display_mode="with_cover",
            extra_info="deny",
            related_user=notif.target,
            related_club=notif.related_club
        )
        return JsonResponse(dict(success=True))
    else:
        return JsonResponse(dict(success=False, message="Undefined Operation Type"))


@require_GET
@login_first
def club_billboard(request):
    limit = request.GET['limit']
    skip = request.GET['skip']
    scope = request.GET['scope']
    filter_type = request.GET['filter']

    latest_version_obj = ClubBillboard.objects.order_by('-version').first()

    if latest_version_obj is None:
        return JsonResponse(dict(success=True, data=[]))

    billboard = ClubBillboard.objects.select_related('club').annotate(
        members_num=Count("club__members")
    ).annotate(
        attended_count=Sum(Case(When(club__members=request.user, then=Value(1)), default=Value(0),
                                output_field=IntegerField()))
    ).filter(
        scope=scope, filter_type=filter_type, version=latest_version_obj.version
    ).order_by('order')[skip: limit + skip]

    for item in billboard:
        club = item.club
        setattr(club, "attended", item.attended_count > 0)

    return JsonResponse(dict(success=True, data=map(
        lambda x: x.dict_description(request.user), billboard
    )))

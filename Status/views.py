# coding=utf-8
from django.views.decorators import http as http_decorator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from .models import Status, StatusLikeThrough, StatusComment, StatusReport
from .forms import StatusCreationForm
from custom.utils import post_data_loader, page_separator_loader, login_first, get_logger
from Notification.signal import send_notification
# Create your views here.

logger = get_logger(__name__)


@http_decorator.require_GET
@login_first
@page_separator_loader
def status_list(request, date_threshold, op_type, limit):
    """ Get the list of status,结构如下:
     -- success
     -- data: array
       | statusID:
       | images:
       | content:
       | created_at:
       | -- car
           | carID
           | name
           | logo
           | image
       | comment_num
       | like_num
       | -- location
           | lat:
           | lon:
           | description
       | -- user
           | user_id:
           | avatar:
           | nick_name:
           | -- avatar_club:
               | id:
               | club_logo:
               | club_name
           | -- avatar_car:
               | carID:
               | name:
               | logo:
               | image:
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    query_type = request.GET.get("query_type", "follow")
    order_by_properties = ["-created_at"]
    if query_type == 'follow':
        # 获取关注的特点
        # content_filter = Q(user__friendship__fans=request.user) | Q(user=request.user)
        content_filter = Q(user=request.user) | Q(user__fans=request.user)
    elif query_type == 'nearby':
        lat = float(request.GET["lat"])
        lon = float(request.GET["lon"])
        distance = float(request.GET["distance"])
        content_filter = Q(location__location__distance_lte=(Point(lon, lat), D(m=distance)))
    elif query_type == "hot":
        # TODO: 剩下一个"热门"需要"实现
        content_filter = Q()
    else:
        return JsonResponse(dict(success=False, message="Undefined query type"))

    data = Status.objects\
        .select_related('user__avatar_club')\
        .select_related('car')\
        .select_related('location')\
        .order_by(*order_by_properties)\
        .filter(date_filter & content_filter, deleted=False)\
        .annotate(comment_num=Count('comments', distinct=True))\
        .annotate(like_num=Count('liked_by', distinct=True))[0:limit]

    data = map(lambda x: x.dict_description(show_liked=True, user=request.user), data)
    return JsonResponse(dict(
        success=True,
        data=data
    ))

@http_decorator.require_GET
@login_first
def status_detail(request, status_id):
    try:
        status = Status.objects \
            .annotate(comment_num=Count('comments', distinct=True)) \
            .annotate(like_num=Count('liked_by', distinct=True))\
            .get(id=status_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="status not found"))
    return JsonResponse(dict(success=True, data=status.dict_description(show_liked=True, user=request.user)))


@http_decorator.require_POST
@login_first
@post_data_loader(json_fields=("inform_of", ))
def post_new_status(request, data):
    form = StatusCreationForm(data, request.FILES)
    if form.is_valid():
        status = form.save()
        if 'inform_of' in data:
            ats = get_user_model().objects.filter(id__in=data['json_data'])
            for at in ats:
                # send_notification.send(sender=get_user_model(),
                #                        message_type="status_inform",
                #                        target=at,
                #                        message_body="",
                #                        related_status=status)
                send_notification.send(
                    sender=Status,
                    target=at,
                    display_mode="with_cover",
                    extra_info="at",
                    related_user=request.user,
                    related_status=status
                )
        return JsonResponse(dict(success=True, data=status.dict_description()))
    else:
        response_dict = dict(success=False)
        response_dict.update(form.errors)
        logger.debug(u"Fail to post new status, the error info is %s" % response_dict)
        return JsonResponse(response_dict)


@http_decorator.require_GET
@login_first
@page_separator_loader
def status_comments(request, date_threshold, op_type, limit, status_id):
    """ 状态评论列表,返回的数据结构为
     ---
      |- success:
      |- comments: list
          |- commentID
          |- created_at
          |- image
          |- content
          |- user
              |- userID
              |- nick_name
              |- avatar
          |- response_to
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)
    try:
        status = Status.objects.get(id=status_id, deleted=False)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code="4002", message="status not found"))
    comments = StatusComment.objects.select_related("user").filter(date_filter, status=status)[0:limit]

    return JsonResponse(dict(
        success=True,
        comments=map(lambda x: x.dict_description(), comments)
    ))


@http_decorator.require_POST
@login_first
@post_data_loader(json_fields=('inform_of', ))
def status_post_comment(request, data, status_id):
    """ 发布评论
     post上来的data的结构为
     :keyword response_to   回复的目标评论，可以不存在
     :keyword inform_of     要@的人的id列表
     :keyword content       评论的文字内容
     :keyword image         评论的图片，从request.FILES中取得
    """
    try:
        status = Status.objects.get(id=status_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='4002', message='Status not found.'))
    if 'response_to' in data:
        try:
            response_to = StatusComment.objects.get(id=data['response_to'])
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code='4002', message='Comments not found.'))
    else:
        response_to = None
    try:
        # Caution: image属性即将废除
        comment = StatusComment.objects.create(user=request.user,
                                               image=request.FILES.get('image', None),
                                               content=data.get('content', None),
                                               response_to=response_to,
                                               status=status)
    except ValidationError:
        logger.debug(u'发表动态评论的时候失败,缺少必要数据。目前提交的内容为%s' % data.get('content', None))
        return JsonResponse(dict(success=False, code='4003', message=u'No valid content found for the comment'))

    if 'inform_of' in data:
        ats = get_user_model().objects.filter(id__in=data['json_data'])
        comment.inform_of.add(*ats)
        for at in ats:
            # send_notification.send(sender=get_user_model(),
            #                        message_type="status_inform",
            #                        target=at,
            #                        message_body="",
            #                        related_status=status)
            send_notification.send(
                sender=StatusComment,
                target=at,
                display_mode="with_cover",
                extra_info="at",
                related_user=request.user,
                related_status=status,
                related_status_comment=comment
            )

    # if the comment replies to another comment, send a notification to the sender of that comment as well.
    if 'response_to' in data:
        # send_notification.send(sender=StatusComment,
        #                        message_type="status_comment_replied",
        #                        target=response_to.user,
        #                        message_body=comment.content,
        #                        related_status_comment=comment,
        #                        related_status=status,
        #                        related_user=comment.user)
        send_notification.send(
            sender=StatusComment,
            target=response_to.user,
            display_mode="with_cover",
            extra_info="response",
            related_user=comment.user,
            related_status=comment.status,
            related_status_comment=comment
        )
        if response_to.user == status.user:
            # avoid duplicated notifications about the same comment
            return JsonResponse(dict(success=True, id=comment.id))
    # send a notification message to the sender of the status
    if status.user != request.user:
        # send_notification.send(sender=Status,
        #                        message_type="status_comment",
        #                        target=status.user,
        #                        message_body=comment.content,
        #                        related_status_comment=comment,
        #                        related_status=status,
        #                        related_user=comment.user)
        send_notification.send(
            sender=StatusComment,
            target=status.user,
            display_mode="with_cover",
            extra_info="response",
            related_user=comment.user,
            related_status=comment.status,
            related_status_comment=comment
        )
    return JsonResponse(dict(success=True, id=comment.id))


@http_decorator.require_POST
@login_first
@post_data_loader()
def status_operation(request, data, status_id):
    if 'op_type' not in data:
        logger.warn(u'动态操作错误')
        return JsonResponse(dict(success=False, code='4300', message='No valid operation type param found.'))
    op_type = data['op_type']
    try:
        status = Status.objects.get(id=status_id, deleted=False)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='4002', message='Status not found.'))

    if op_type == 'like':
        # 点赞
        obj, created = StatusLikeThrough.objects.get_or_create(user=request.user,
                                                               status=status)
        if not created:
            obj.delete()
        elif status.user != request.user:
            # send_notification.send(sender=Status,
            #                        message_type="status_like",
            #                        related_user=request.user,
            #                        related_status=status,
            #                        target=status.user,
            #                        message_body="")
            status.recent_like_user = request.user
            status.save()
            send_notification.send(
                sender=Status,
                target=status.user,
                display_mode="with_cover",
                extra_info="like",
                related_user=request.user,
                related_status=status
            )
        result = dict(
            like_state=created,
            like_num=StatusLikeThrough.objects.filter(status=status).count()
        )
        return JsonResponse(dict(success=True, like_info=result))
    elif op_type == "delete":
        # 删除
        if status.user != request.user:
            # no permission
            logger.warning(u'动态删除权限问题, 参与用户id:{user_id}, 涉及动态为{status_id}'.format(
                user_id=request.user.id,
                status_id=status.id
            ))
            return JsonResponse(dict(success=False, code="code", message="no permission"))
        status.deleted = True
        status.save()
        return JsonResponse(dict(success=True))
    elif op_type == "report":
        StatusReport.objects.get_or_create(
            user=request.user,
            status=status,
            reason=data["reason"]
        )
        return JsonResponse(dict(success=True))
    else:
        logger.warning(u"非法操作, 涉及用户为%s" % request.user.id)
        return JsonResponse(dict(success=False, code='4004', message='Operation not defined'))


@http_decorator.require_GET
@login_first
@page_separator_loader
def status_like_users(request, date_threshold, op_type, limit, status_id):
    try:
        status = Status.objects.get(id=status_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='4002', message='Status not found.'))

    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    likes = StatusLikeThrough.objects.select_related("user")\
        .filter(status=status).filter(date_filter, stauts=status)\
        .order_by("-like_at")[0:limit]
    return JsonResponse(dict(
        success=True,
        data=map(lambda x: x.user.dict_description(), likes)
    ))

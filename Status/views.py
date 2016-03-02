# coding=utf-8
from django.views.decorators import http as http_decorator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from .models import Status, StatusLikeThrough, StatusComment
from Profile.models import UserRelationSetting
from .forms import StatusCreationForm
from custom.utils import post_data_loader, page_separator_loader, login_first
# Create your views here.


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

    if query_type == 'follow':
        # 获取关注的特点
        # content_filter = Q(user__friendship__fans=request.user) | Q(user=request.user)
        content_filter = Q()
    elif query_type == 'nearby':
        lat = request.GET["lat"]
        lon = request.GET["lon"]
        distance = request.GET["distance"]
        content_filter = Q(location__distance_lte=(Point(lon, lat), D(m=distance)))
    else:
        # TODO: 剩下一个"热门"需要"实现
        content_filter = Q()

    # 这里我们认为黑名单的长度是有限的,故将黑名单全部载入内存然后筛选
    blacklist1 = UserRelationSetting.objects.filter(
        user=request.user, see_his_status=False
    ).values_list("target__id")
    blacklist2 = UserRelationSetting.objects.filter(
        target=request.user, allow_see_status=False
    ).values_list("target__id")
    blacklist = list(blacklist1) + list(blacklist1)
    blacklist_filter = ~Q(user__id__in=blacklist)

    data = Status.objects\
        .select_related('user__profile__avatar_club')\
        .select_related('car')\
        .select_related('location')\
        .order_by("-created_at")\
        .filter(date_filter & content_filter & blacklist_filter, deleted=False)\
        .annotate(comment_num=Count('comments'))\
        .annotate(like_num=Count('liked_by'))[0:limit]

    data = map(lambda x: x.dict_description(), data)
    return JsonResponse(dict(
        success=True,
        data=data
    ))


@http_decorator.require_POST
@login_first
@post_data_loader()
def post_new_status(request, data):
    form = StatusCreationForm(data, request.FILES)
    if form.is_valid():
        status = form.save()
        return JsonResponse(dict(success=True, statusID=status.id))
    else:
        response_dict = dict(success=False)
        response_dict.update(form.errors)
        print(response_dict)
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
    comments = StatusComment.objects.select_related("user__profile").filter(date_filter, status=status)[0:limit]

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
            return JsonResponse(dict(success=False, code='4002', message='Status not found.'))
    else:
        response_to = None
    try:
        comment = StatusComment.objects.create(user=request.user,
                                               image=request.FILES.get('image', None),
                                               content=data.get('content', None),
                                               response_to=response_to,
                                               status=status)
    except ValidationError:
        return JsonResponse(dict(success=False, code='4003', message=u'No valid content found for the comment'))

    if 'inform_of' in data:
        ats = get_user_model().objects.filter(id__in=data['json_data'])
        comment.inform_of.add(*ats)
    return JsonResponse(dict(success=True))


@http_decorator.require_POST
@login_first
@post_data_loader()
def status_operation(request, data, status_id):
    if 'op_type' not in data:
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
        return JsonResponse(dict(success=True, like_state=created))
    elif op_type == "delete":
        # 删除
        if status.user != request.user:
            # no permission
            return JsonResponse(dict(success=False, code="code", message="no permission"))
        status.deleted = True
        status.save()
        return JsonResponse(dict(success=True))
    else:
        return JsonResponse(dict(success=False, code='4004', message='Operation not defined'))

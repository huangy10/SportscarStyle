# coding=utf-8
from django.views.decorators import http as http_decorator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model

from .models import Status, StatusLikeThrough, StatusComment
from .forms import StatusCreationForm
from custom.utils import post_data_loader, page_separator_loader, login_first
# Create your views here.


@http_decorator.require_GET
@login_first
@page_separator_loader
def status_list(request, date_threshold, op_type, limit):
    """ Get the list of status
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    data = Status.objects\
        .select_related('user__profile__avatar_club')\
        .select_related('car')\
        .select_related('location')\
        .filter(date_filter)\
        .annotate(comment_num=Count('comments'))\
        .annotate(like_num=Count('liked_by'))[0:limit]

    def format_fix(status):
        result = dict()
        result['id'] = status.id
        result['created_at'] = status.created_at.strftime('%Y-%m-%d %H-%M-%S %Z')
        result['image'] = status.image.url
        result['content'] = status.content
        if status.car is not None:
            result['car'] = dict(name=status.car.name, logo=status.car.logo.url, id=status.car.id)
        result['comment_num'] = status.comment_num
        result['like_num'] = status.like_num
        if status.location is not None:
            location = status.location
            result['location'] = dict(description=location.description, lat=location.latitude, lon=location.longitude)
        user_dict = dict(id=status.user.id, avatar=status.user.profile.avatar.url)
        if status.user.profile.avatar_club is not None:
            user_dict['club'] = dict(id=status.user.profile.avatar_club.id,
                                     image=status.user.profile.avatar_club.logo.url)
        result['user'] = user_dict
        return result

    data = map(format_fix, data)
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
        form.save()
        return JsonResponse(dict(success=True))
    else:
        response_dict = dict(success=False)
        response_dict.update(form.errors)
        return JsonResponse(response_dict)


@http_decorator.require_GET
@login_first
@page_separator_loader
def status_comments(request, date_threshold, op_type, limit, status_id):
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)
    comments = StatusComment.objects.filter(date_filter, status__id=status_id). \
        values('id', 'user__profile__nick_name', 'user__id', 'created_at', 'image', 'response_to__id', 'id')[0:limit]

    def format_fix(comment):
        # comment['image'] = settings.MEDIA_URL + comment['image']
        comment['user_id'] = comment['user__id']
        comment['user_nickname'] = comment['user__profile__nick_name']
        comment['created_at'] = comment['created_at'].strftime('%Y-%m-%d %H:%M:%S %Z')
        del comment['user__id']
        del comment['user__profile__nick_name']
        return comment

    comments = map(format_fix, comments)
    return JsonResponse(dict(
        success=True,
        comments=list(comments)
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
        status = Status.objects.get(id=status_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='4002', message='News not found.'))
    if op_type == 'like':
        obj, created = StatusLikeThrough.objects.get_or_create(user=request.user,
                                                               status=status)
        if not created:
            obj.delete()
        return JsonResponse(dict(success=True, like_state=created))
    else:
        return JsonResponse(dict(success=False, code='4004', message='Operation not defined'))

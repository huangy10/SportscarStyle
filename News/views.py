# coding=utf-8
from django.http import JsonResponse
from django.views.decorators import http as http_decorators
from django.db.models import Q, Count, Case, When, BooleanField, Value, CharField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import News, NewsComment, NewsLikeThrough
from custom.utils import login_first, post_data_loader, page_separator_loader


# Create your views here.


@http_decorators.require_GET
@login_first
@page_separator_loader
def news_list(request, date_threshold, op_type, limit):
    """ Get the host page of news module
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    data = News.objects.filter(date_filter) \
               .annotate(comment_num=Count('comments')) \
               .annotate(like_num=Count('liked_by')) \
               .values()[0: limit]

    def format_fix(image_field):
        # image_field['cover'] = settings.MEDIA_URL + image_field['cover']
        image_field['created_at'] = image_field['created_at'].strftime('%Y-%m-%d %H-%M-%S %Z')
        return image_field

    data = map(format_fix, list(data))

    return JsonResponse(dict(
        success=True,
        news=data
    ))


@http_decorators.require_GET
@login_first
def news_detail(requset, news_id):
    """ 该接口用来获取制定id的资讯，没有出现在news_list上的额外信息，
     暂时这个接口用来返回最近点赞的人
    """
    try:
        news = News.objects.prefetch_related('liked_by__profile').get(id=news_id)
        recent_like = news.liked_by.all().first()
        if recent_like is None:
            return JsonResponse(dict(success=True, recent_like=''))
        else:
            return JsonResponse(dict(success=True, recent_like=recent_like.profile.nick_name))
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='3000', message='News not found.'))


@http_decorators.require_GET
@login_first
@page_separator_loader
def news_comments_list(request, date_threshold, op_type, limit, news_id):
    """ Fetch comments from this interface
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)
    comments = NewsComment.objects.filter(date_filter, news__id=news_id). \
        values('user__profile__nick_name', 'user__id', 'created_at', 'image', 'response_to__id', 'id')[0: limit]

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


@http_decorators.require_POST
@login_first
@post_data_loader(json_fields=('inform_of', ))
def news_post_comment(request, data, news_id):
    """ 发布评论
    """
    try:
        news = News.objects.get(id=news_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='3000', message='News not found.'))
    if 'response_to' in data:
        try:
            response_to = NewsComment.objects.get(id=data['response_to'])
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code='3001', message='News comment not found.'))
    else:
        response_to = None
    try:
        comment = NewsComment.objects.create(user=request.user,
                                             image=request.FILES.get('image', None),
                                             content=data.get('content', None),
                                             response_to=response_to,
                                             news=news)
    except ValidationError:
        return JsonResponse(dict(success=False, code='3003', message=u'No valid content found for the comment'))

    if 'inform_of' in data:
        for at in data['json_data']:
            try:
                inform_user = get_user_model().objects.get(id=at)
                comment.inform_of.add(inform_user)
            except ObjectDoesNotExist:
                return JsonResponse(dict(success=False, code='3002', message='User with id %s not found' % at))
    return JsonResponse(dict(success=True))


@http_decorators.require_POST
@login_first
@post_data_loader()
def news_operation(request, data, news_id):
    """ 对资讯进行炒作，目前仅支持点赞
    """
    if 'op_type' not in data:
        return JsonResponse(dict(success=False, code='3301', message='No valid operation type param found.'))
    op_type = data['op_type']
    try:
        news = News.objects.get(id=news_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='3001', message='News not found.'))
    if op_type == 'like':
        obj, created = NewsLikeThrough.objects.get_or_create(user=request.user,
                                                             news=news)
        if not created:
            obj.delete()
        return JsonResponse(dict(success=True, like_state=created))
    else:
        return JsonResponse(dict(success=False, code='3004', message='Operation not defined'))

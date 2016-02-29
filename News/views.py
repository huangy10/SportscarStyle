# coding=utf-8
import os

from django.http import JsonResponse
from django.views.decorators import http as http_decorators
from django.db.models import Q, Count, Case, When, BooleanField, Value, CharField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import News, NewsComment, NewsLikeThrough
from custom.utils import login_first, post_data_loader, page_separator_loader
from Profile.models import UserFollow


# Create your views here.


@http_decorators.require_GET
@login_first
@page_separator_loader
def news_list(request, date_threshold, op_type, limit):
    """ Get the host page of news module
     ---
      |- success:
      |- news:
         |- id
         |- cover
         |- created_at
         |- content
         |- title
         |- like_num
         |- comment_num
         |- recent_like_user_id            # 最近的改用户的好友中赞了这个资讯的人的id
    """
    # TODO: 这里更改了返回的结构,新的结构参加上面的注释
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    data = News.objects.filter(date_filter) \
               .annotate(comment_num=Count('comments')) \
               .annotate(like_num=Count('liked_by'))[0: limit]

    def format_fix(news):
        result = dict(
            id=news.id,
            cover=news.cover.url,
            created_at=news.created_at.strftime('%Y-%m-%d %H:%M:%S %Z'),
            content=news.content,
            title=news.title,
            like_num=news.like_num,
            comment_num=news.like_num,
            liked=NewsLikeThrough.objects.filter(user=request.user, news=news).exists()
        )
        most_recent_like_record = NewsLikeThrough.objects.filter(user__friendship__friend=request.user, news=news)\
            .order_by("-like_at").first()
        if most_recent_like_record is not None:
            result["recent_like_user_id"] = most_recent_like_record.user_id
        return result

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
       The architecture of the response JSON object is:
        ---
         |- success:
         |- comments: list:
            |- commentID:
            |- created_at
            |- image:
            |- content:
            |- user:                    # profile的simple_dict_description生成的结构
               |- userID
               |- nick_namne
               |- avatar
            |- response_to:
    """
    # TODO: 变更了评论列表返回的形式,变更之后的格式见上面的注释
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)
    comments = NewsComment.objects.filter(date_filter, news__id=news_id).select_related("user__profile")[0: limit]

    def format_fix(comment):
        user = comment.user
        result = dict(
            commentID=comment.id,
            content=comment.content,
            user=user.profile.simple_dict_description(),
            created_at=comment.created_at.strftime('%Y-%m-%d %H:%M:%S %Z')
        )
        if comment.image:
            result["image"] = comment.image.url
        if comment.response_to is not None:
            result["response_to"] = comment.response_to_id
        return result

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
     需要返回分配给评论的id
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
    return JsonResponse(dict(success=True, id=comment.id))


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
        result =dict(
            like_state=created,
            like_num=NewsLikeThrough.objects.filter(news=news).count()
        )
        return JsonResponse(dict(success=True, like_info=result))
    else:
        return JsonResponse(dict(success=False, code='3004', message='Operation not defined'))

# coding=utf-8
import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings

from custom.utils import path_creator
from custom.models_template import BaseCommentManager, comment_image_path
# Create your models here.


def cover_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('cover_path', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


def video_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('video_path', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class News(models.Model):
    """首页资讯的信息,

    注意这里评论部分由Comment模块统一处理
    """
    cover = models.ImageField(upload_to=cover_path, verbose_name=u'封面', null=True)
    title = models.CharField(max_length=255, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'正文')
    video = models.FileField(upload_to=video_path, verbose_name=u'视频', null=True)

    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_news', verbose_name=u'点赞',
                                      through='NewsLikeThrough')
    shared_times = models.PositiveIntegerField(default=0, verbose_name=u'被分享次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建日期')

    class Meta:
        verbose_name = u'资讯'
        verbose_name_plural = u'资讯'
        ordering = ('-created_at', )


class NewsComment(models.Model):
    """针对资讯的评论
    """
    news = models.ForeignKey(News, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'发布用户', related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间', blank=True)
    image = models.ImageField(upload_to=comment_image_path, verbose_name=u'评论图片', blank=True)
    content = models.CharField(max_length=255, verbose_name=u'评论正文', null=True, blank=True)
    response_to = models.ForeignKey('self', related_name='responses', null=True)
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'@某人',
                                       related_name='news_comments_need_to_see')
    objects = BaseCommentManager()

    class Meta:
        abstract = False
        verbose_name_plural = u'咨询评论'
        verbose_name = u'咨询评论'


class NewsLikeThrough(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    news = models.ForeignKey(News)
    like_at = models.DateTimeField(auto_now_add=True)

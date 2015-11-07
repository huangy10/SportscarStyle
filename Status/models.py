# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from custom.models_template import BaseCommentManager, comment_image_path
# Create your models here.


def status_image_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('cover_path', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class Status(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图')
    content = models.CharField(max_length=255, verbose_name=u'正文')
    location = models.ForeignKey('Location.Location', verbose_name=u'发布地点')
    car = models.ForeignKey('Sportscar.Sportscar', verbose_name=u'签名跑车')

    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'点赞', related_name='liked_status',
                                      through='StatusLikeThrough')
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'提醒谁看',
                                       related_name='status_need_to_see')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'发布日期')

    class Meta:
        verbose_name = u'状态'
        verbose_name_plural = u'状态'


class StatusComment(models.Model):

    status = models.ForeignKey(Status, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'发布用户', related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间', blank=True)
    image = models.ImageField(upload_to=comment_image_path, verbose_name=u'评论图片')
    content = models.CharField(max_length=255, verbose_name=u'评论正文', null=True, blank=True)
    response_to = models.ForeignKey('self', related_name='responses', null=True, blank=True)
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'@某人',
                                       related_name='status_comments_need_to_see')
    objects = BaseCommentManager()

    class Meta:
        abstract = False
        verbose_name = u'状态评论'
        verbose_name_plural = u'状态评论'


class StatusLikeThrough(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.ForeignKey(Status)
    like_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'status')

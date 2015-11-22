# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from custom.models_template import comment_image_path, BaseCommentManager
# Create your models here.


def activity_poster(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".format(
        'activity_poster',
        current.year,
        current.month,
        current.day,
        random_file_name,
        ext
    )
    return new_file_name


class Activity(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'活动名称')
    description = models.TextField(verbose_name=u'活动描述')

    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'通知谁看',
                                       related_name='activities_need_to_see')
    max_attend = models.PositiveIntegerField(default=0, verbose_name=u'人数上限')
    start_at = models.DateTimeField(verbose_name=u'开始时间')
    end_at = models.DateTimeField(verbose_name=u'结束时间')
    allowed_club = models.ForeignKey('Club.Club', verbose_name=u'允许加入的俱乐部', blank=True, null=True)
    poster = models.ImageField(upload_to=activity_poster, verbose_name=u'活动海报')
    location = models.ForeignKey('Location.Location', verbose_name=u'活动地点')

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = u'活动'
        verbose_name_plural = u'活动'


class ActivityJoin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    activity = models.ForeignKey(Activity, related_name='+')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ActivityComment(models.Model):

    activity = models.ForeignKey(Activity, verbose_name='相关活动', related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=comment_image_path, verbose_name='评论图片')
    content = models.CharField(max_length=255, verbose_name='评论正文')
    response_to = models.ForeignKey('self', related_name='responses', null=True, blank=True)
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='@某人',
                                       related_name='activity_comments_need_to_see')

    objects = BaseCommentManager()

    class Meta:
        verbose_name = '活动评论'
        verbose_name_plural = '活动评论内容'

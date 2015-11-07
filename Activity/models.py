# coding=utf-8
from django.db import models
from django.conf import settings
# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'活动名称')
    description = models.TextField(verbose_name=u'活动描述')

    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'通知谁看',
                                       related_name='activities_need_to_see')
    max_attend = models.PositiveIntegerField(default=0, verbose_name=u'人数上限')
    start_at = models.DateTimeField(verbose_name=u'开始时间')
    end_at = models.DateTimeField(verbose_name=u'结束时间')
    allowed_club = models.ForeignKey('Club.Club', verbose_name=u'允许加入的俱乐部', blank=True)
    location = models.ForeignKey('Location.Location', verbose_name=u'活动地点')

    class Meta:
        verbose_name = u'活动'
        verbose_name_plural = u'活动'


class ActivityJoin(models.Model):
    pass
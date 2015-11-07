# coding=utf-8
from django.contrib.gis.db import models
from django.conf import settings
# Create your models here.


class Location(models.Model):
    location = models.PointField(verbose_name=u'当前位置')
    description = models.CharField(max_length=255, verbose_name=u'地理信息描述')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'位置更新时间')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='location', verbose_name=u'用户名')

    objects = models.GeoManager()

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x

    class Meta:
        verbose_name = u'位置'
        verbose_name_plural = u'位置'

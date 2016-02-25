# coding=utf-8
from django.contrib.gis.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.geos import Point

# Create your models here.


class Location(models.Model):
    location = models.PointField(verbose_name=u'当前位置')
    description = models.CharField(max_length=255, verbose_name=u'地理信息描述')

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

    def dict_description(self):
        return dict(
            lon=self.longitude, lat=self.latitude, description=self.description
        )


class UserTracking(models.Model):
    """ 这个表是存储的是用户的事实位置.
     注意,更新用户位置时,重新创建新的条目,而非是更改这里的location
    """
    location = models.ForeignKey(Location, verbose_name='位置')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='用户', related_name="location")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    location_available = models.BooleanField(default=False, verbose_name="地址数据是否可用")

    class Meta:
        ordering = ('-created_at', )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def auto_create_tracking(sender, instance, created, **kwargs):
    """ 自动创建用户位置跟踪对象
    """
    if created:
        loc = Location.objects.create(location=Point(0, 0), description="")
        UserTracking.objects.get_or_create(user=sender, location=loc)


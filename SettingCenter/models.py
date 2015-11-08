# coding=utf-8
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class SettingCenter(models.Model):
    """用户设置中心，存储用户的设置信息
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='setting_center')

    notification_accept = models.BooleanField(default=True, verbose_name=u'接受通知')
    notification_sound = models.BooleanField(default=True, verbose_name=u'声音')
    notification_shake = models.BooleanField(default=True, verbose_name=u'震动')

    blacklist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+')

    location_visible_to = models.CharField(max_length=10, choices=(
        ('all', '所有人'),
        ('female_only', '仅女性'),
        ('male_only', '仅男性'),
        ('none', '不可见'),
        ('only_idol', '仅我关注的人'),
        ('only_fried', '互相关注')
    ), default='all')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def auto_create_setting_center(sender, instance, created, **kwargs):
    if created:
        setting_center, _ = SettingCenter.objects.get_or_create(user=instance)


class Suggestion(models.Model):

    content = models.CharField(max_length=255, verbose_name='内容')
    setting_center = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


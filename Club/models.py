# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils.encoding import smart_str
from django.utils import timezone

# Create your models here.


class ClubJoining(models.Model):
    """这里定义了用户关于一个群聊的设置
    """
    # Basic information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户")
    nick_name = models.CharField(max_length=100, verbose_name=u"本群昵称")
    club = models.ForeignKey("Club.Club", verbose_name=u"俱乐部")
    join_date = models.DateTimeField(auto_now_add=True, verbose_name=u"加入日期")

    # Settings
    show_nick_name = models.BooleanField(default=True, verbose_name=u"显示本群成员昵称")
    no_disturbing = models.BooleanField(default=False, verbose_name=u"消息免打扰")
    always_on_top = models.BooleanField(default=False, verbose_name=u"置顶聊天")
    always_on_to_date = models.DateTimeField(null=True, blank=True, verbose_name=u"置顶的日期")  # 影响排序

    unread_chats = models.IntegerField(default=0, verbose_name=u"未读消息数量")

    def __str__(self):
        return smart_str("{0} in {1}".format(self.user.profile.nick_name, self.club.name))

    class Meta:
        unique_together = ("user", "club")

    def dict_description(self, show_members=False, for_host=False):
        """
         :param show_members 是否打包成员信息
         :param for_host     以host权限获取数据
        """
        result = dict(
            nick_name=self.nick_name,
            club=self.club.dict_description(show_members=show_members,
                                            show_setting=for_host),
            show_nick_name=self.show_nick_name,
            no_disturbing=self.show_nick_name,
            always_on_top=self.always_on_top,
        )
        return result


def club_logo(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('club_logo', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class ClubManager(models.Manager):
    """ 自动将创建者加入俱乐部的功能在这里实现
    """

    def create(self, *args, **kwargs):
        obj = super(ClubManager, self).create(*args, **kwargs)
        host = kwargs.get('host')
        ClubJoining.objects.create(user=host,
                                   club=obj,
                                   nick_name=host.profile.nick_name)
        return obj


class Club(models.Model):
    """这是对俱乐部的一个抽象
    """
    name = models.CharField(max_length=100, verbose_name=u"俱乐部名称")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"发起者", related_name='club_started')
    logo = models.ImageField(upload_to=club_logo, verbose_name=u"俱乐部标识")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u"成员", through='ClubJoining')
    description = models.TextField(verbose_name=u"俱乐部简介")
    identified = models.BooleanField(default=False, verbose_name="是否认证")
    identified_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u"创建日期")

    objects = ClubManager()

    # some settings about club
    only_host_can_invite = models.BooleanField(default=False, verbose_name=u"只有群主能够邀请")
    show_members_to_public = models.BooleanField(default=False, verbose_name=u"对外公布成员信息")

    def __str__(self):
        return smart_str(self.name)

    class Meta:
        verbose_name = u"俱乐部"
        verbose_name_plural = u'俱乐部'

    def dict_description(self, show_members=False, show_setting=False):
        result = dict(
            id=self.id, club_logo=self.logo.url,
            club_name=self.name, description=self.description,
            identified=self.identified
        )
        if show_members:
            result.update(
                members=map(lambda x: x.profile.simple_dict_description(), self.members.all())
            )
        if show_setting:
            result.update(dict(
                only_host_can_invite=self.only_host_can_invite,
                show_members_to_public=self.show_members_to_public
            ))
        return result

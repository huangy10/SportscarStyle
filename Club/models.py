# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.encoding import smart_str
from django.utils import timezone

# Create your models here.

from Sportscar.models import SportCarOwnership, Sportscar


class ClubJoining(models.Model):
    """这里定义了用户关于一个群聊的设置
    """
    # Basic information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户", related_name="clubs")
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
        return smart_str(u"{0} in {1}".format(self.user.nick_name, self.club.name))

    class Meta:
        unique_together = ("user", "club")

    def dict_description(self, show_members=False, for_host=False, show_members_num=False):
        """
         :param show_members 是否打包成员信息
         :param for_host     以host权限获取数据
        """
        result = dict(
            id=self.id,
            nick_name=self.nick_name,
            club=self.club.dict_description(show_members=show_members,
                                            show_setting=for_host,
                                            show_members_num=show_members_num),
            show_nick_name=self.show_nick_name,
            no_disturbing=self.no_disturbing,
            always_on_top=self.always_on_top,
        )
        return result

    def update_settings(self, settings, update_club=False):
        """ 更新设置
         :param settings        dict like object
         :param update_club     Boolean, whether to update the club object
        """
        if update_club:
            self.club.update_settings(settings)
        self.show_nick_name = settings.get("show_nick_name", self.show_nick_name)
        self.no_disturbing = settings.get("no_disturbing", self.no_disturbing)
        self.always_on_top = settings.get("always_on_top", self.always_on_top)
        self.nick_name = settings.get("nick_name", self.nick_name)
        self.save()


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
                                   nick_name=host.nick_name)
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
    city = models.CharField(max_length=30, verbose_name=u"俱乐部所在的城市")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u"创建日期")

    value_total = models.IntegerField(default=0, verbose_name=u"俱乐部中所有成员的所有认证车辆的官方参考价格总和")
    value_average = models.IntegerField(default=0, verbose_name=u"均价")

    objects = ClubManager()

    # some settings about club
    only_host_can_invite = models.BooleanField(default=False, verbose_name=u"只有群主能够邀请")
    show_members_to_public = models.BooleanField(default=False, verbose_name=u"对外公布成员信息")

    # status
    deleted = models.BooleanField(default=False, verbose_name=u"俱乐部是否被删除")

    def __str__(self):
        return smart_str(self.name)

    class Meta:
        verbose_name = u"俱乐部"
        verbose_name_plural = u'俱乐部'

    def dict_description(self, show_members=False,
                         show_setting=False,
                         show_value=False,
                         show_members_num=False,
                         show_attended=False,
                         target_user=None):
        value = ClubJoining.objects.filter(club=self).aggregate(value=Sum("user__value"))["value"]
        result = dict(
            id=self.id, club_logo=self.logo.url,
            club_name=self.name, description=self.description,
            identified=self.identified, city=self.city,
            host=self.host.dict_description(),
            value_total=value,
        )
        if show_members:
            from Club.views import CLUB_MEMBERS_DISPLAY_NUM
            result.update(
                members=map(lambda x: x.dict_description(), self.members.all()[0: CLUB_MEMBERS_DISPLAY_NUM])
            )
        if show_setting:
            result.update(dict(
                only_host_can_invite=self.only_host_can_invite,
                show_members_to_public=self.show_members_to_public
            ))
        if show_value:
            result.update(dict(
                value=self.value_total
            ))
        if show_members_num:
            if hasattr(self, "members_num"):
                result.update(
                    members_num=self.members_num,
                    value_average=value / self.members_num
                )
            else:
                member_num = ClubJoining.objects.filter(club=self).count()
                result.update(
                    members_num=member_num,
                    value_average=value / member_num
                )
        if show_attended:
            if hasattr(self, "attended"):
                result.update(attended=self.attended)
            else:
                result.update(attended=ClubJoining.objects.filter(
                    user=target_user, club=self
                ).exists())
        return result

    def update_settings(self, settings):
        self.name = settings.get("name", self.name)
        self.only_host_can_invite = settings.get("only_host_can_invite", self.only_host_can_invite)
        self.show_members_to_public = settings.get("show_members_to_public", self.show_members_to_public)
        self.description = settings.get("description", self.description)
        self.save()

    def recalculate_value(self, commit=True):
        self.value_total = ClubJoining.objects.filter(club=self)\
            .aggregate(total=models.Sum("user__value"))["total"] or 0
        self.value_average = self.value_total / ClubJoining.objects.filter(club=self).count()
        if commit:
            self.save()


class ClubAuthRequest(models.Model):
    """ 俱乐部认证
    """
    approve = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    club = models.ForeignKey("Club.Club", verbose_name="待认证的俱乐部")
    city = models.CharField(max_length=100, verbose_name="俱乐部所处的城市", default="")
    description = models.CharField(max_length=100, verbose_name="俱乐部简介", default="")

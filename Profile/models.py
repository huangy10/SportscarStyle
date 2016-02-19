# coding=utf-8
import uuid
import datetime
import os

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.encoding import smart_str
from django.utils.functional import cached_property
# Create your models here.

DEFAULT_AVATAR_NAME = 'default_avatar.png'


class ProfileTag(models.Model):
    tag_type = models.CharField(max_length=25, verbose_name=u'标签类型',
                                choices=(
                                    ('job', u'行业'),
                                    ('interest', u'兴趣'),
                                ))
    tag_name = models.CharField(max_length=25, verbose_name=u'标签显示的名称')
    helper_text = models.CharField(max_length=255, verbose_name=u'帮助信息')

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


def profile_avatar(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".format(
        'profile_avatar',
        current.year,
        current.month,
        current.day,
        random_file_name,
        ext
    )
    return new_file_name


def auth_image(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".format(
        'auth_image',
        current.year,
        current.month,
        current.day,
        random_file_name,
        ext
    )
    return new_file_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        profile, _ = UserProfile.objects.get_or_create(user=instance,
                                                       nick_name='DEFAULT NAME',
                                                       birth_date=datetime.date(year=1970, month=1, day=1),
                                                       avatar=os.path.join('defaults', DEFAULT_AVATAR_NAME),
                                                       gender='m',
                                                       )
        FriendShip.objects.get_or_create(creator=instance)


class UserProfile(models.Model):
    """这个model提供对于用户的基本信息的描述
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    # Base information about the user
    nick_name = models.CharField(max_length=63, verbose_name=u'昵称', help_text=u'用户昵称')
    avatar = models.ImageField(upload_to=profile_avatar, verbose_name=u'头像')
    avatar_club = models.ForeignKey('Club.Club', verbose_name=u'认证俱乐部', null=True, blank=True)
    avatar_car = models.ForeignKey('Sportscar.Sportscar', verbose_name=u'头像边的跑车', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', u'男'),
        ('f', u'女'),
    ), verbose_name=u'性别')
    birth_date = models.DateField(verbose_name=u'出生日期')
    star_sign = models.CharField(max_length=25, choices=(
        ('Aries', u'白羊座'),
        ('Taurus', u'金牛座'),
        ('Gemini', u'双子座'),
        ('Cancer', u'巨蟹座'),
        ('Leo', u'狮子座'),
        ('Virgo', u'处女座'),
        ('Libra', u'天秤座'),
        ('Scorpio', u'天蝎座'),
        ('Sagittarius', u'射手座'),
        ('Capricorn', u'摩羯座'),
        ('Aquarius', u's水瓶座'),
        ('Pisces', u'双鱼座'),
    ), verbose_name=u'星座', default='Aries')

    district = models.CharField(max_length=255, verbose_name=u'地区', default='')
    signature = models.CharField(max_length=255, verbose_name=u'签名', default='')
    job = models.CharField(max_length=64, verbose_name='行业', default='')

    corporation_user = models.BooleanField(default=False, verbose_name="是否是经过认证的企业用户")

    @property
    def age(self):
        current = timezone.now().date()
        d_year = current.year - self.birth_date.year
        if current.month < self.birth_date.month \
                or (current.month == self.birth_date.month and current.day < self.birth_date.day):
            d_year -= 1

        return d_year

    def __str__(self):
        return smart_str(self.nick_name)

    def simple_dict_description(self):
        return dict(
            userID=self.user_id,
            nick_name=self.nick_name,
            avatar=self.avatar.url
        )

    def complete_dict_description(self):
        result = self.simple_dict_description()
        if self.avatar_club is not None:
            result["avatar_club"] = self.avatar_club.dict_description()
        if self.avatar_car is not None:
            result["avatar_car"] = self.avatar_car.dict_description()
        return result

    class Meta:
        verbose_name = u'用户详情'
        verbose_name_plural = u'用户详情'


class UserFollow(models.Model):
    """ 描述用户关注行为的列表
    """
    source_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name='关注者')
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', verbose_name='被关注者')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return smart_str("%s --> %s" % (self.source_user.username, self.target_user.username))

    class Meta:
        verbose_name = u'用户关系'
        verbose_name_plural = u'用户关系'
        ordering = ['-created_at', ]
        unique_together = ("source_user", "target_user")


@receiver(post_save, sender=UserFollow)
def auto_maintain_friendship(sender, instance, created, **kwargs):
    """ 当创建UserFollow对象时维护相应的friendship对象
    """
    if created:
        source_user = instance.source_user
        target_user = instance.target_user
        source_user.friendship.follow.add(target_user)
        target_user.friendship.fans.add(source_user)
        if UserFollow.objects.filter(source_user=target_user, target_user=source_user).exists():
            source_user.friendship.friend.add(target_user)
            target_user.friendship.friend.add(source_user)


@receiver(post_delete, sender=UserFollow)
def auto_delete_friendship(sender, instance, **kwargs):
    """ 在删除UserFollow时自动维护这个FriendShip索引
    """
    source_user = instance.source_user
    target_user = instance.target_user
    target_user.friendship.friend.remove(source_user)
    target_user.friendship.fans.remove(source_user)
    source_user.friendship.friend.remove(target_user)
    source_user.friendship.follow.remove(target_user)


class FriendShip(models.Model):
    """ 为了快速检索用户朋友关系而建立的索引表.是对上面的UserFollow表的补充, 需要由上面的UserFollow来自动维护
    """
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="friendship", verbose_name="朋友圈创建者")
    friend = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="does_not_important_1", verbose_name="朋友")
    fans = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="does_not_important_2", verbose_name="粉丝")
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="does_not_important_3", verbose_name="关注")


class UserRelationSetting(models.Model):
    """ 用户关系设置,主要是的昵称,是否允许查看状态等
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="relation_settings")
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")

    allow_see_status = models.BooleanField(default=True, verbose_name="允许查看我的动态")
    see_his_status = models.BooleanField(default=True, verbose_name="是否查看他的动态")
    remark_name = models.CharField(max_length=255, verbose_name="备注名称")

    blacklist_at = models.DateTimeField(verbose_name="拉黑时间", auto_now_add=True)

    @property
    def see_status(self):
        return self.allow_see_status and self.see_his_status

    def dict_description(self):
        return dict(
            user=self.user.profile.simple_dict_description(),
            target=self.target.profile.simple_dict_description(),
            remark_name=self.remark_name,
            see_his_status=self.see_his_status,
            allow_see_status=self.allow_see_status,
            blacklist_at=self.blacklist_at.strftime('%Y-%m-%d %H:%M:%S %Z')
        )


class AuthenticationManager(models.Manager):

    def already_sent(self, phone, seconds=60):
        """ Check if a valid authentication code has already sent to the given phone
         number in `seconds`

         :param phone phone number
         :param seconds time threshold
        """
        if AuthenticationCode.objects.filter(phone_num=phone, is_active=True).exists():
            record = AuthenticationCode.objects.filter(phone_num=phone, is_active=True).first()
            if (timezone.now() - record.created_at).total_seconds() > seconds:
                AuthenticationCode.objects.filter(phone_num=phone).update(is_active=False)
                return False
            else:
                return True
        else:
            return False

    def check_code(self, code, phone, seconds=60*5):
        """ Check the code
         :param code authentication code
         :param phone phone number
         :param seconds expire time
         :return boolean
        """
        record = AuthenticationCode.objects.filter(phone_num=phone, code=code, is_active=True).first()
        if record is None:
            return False
        elif (timezone.now() - record.created_at).total_seconds() > seconds:
            return False
        else:
            return True

    def deactivate(self, code, phone):
        """ Deactivate a code
         :param code authentication code
         :param phone corresponding phone number
         :return True on success
        """
        try:
            record = AuthenticationCode.objects.get(phone_num=phone, code=code)
            record.is_active = False
            record.save()
            return True
        except ObjectDoesNotExist:
            return False


class AuthenticationCode(models.Model):
    phone_num = models.CharField(max_length=20, verbose_name=u'手机号码')
    code = models.CharField(max_length=6, verbose_name=u'验证码')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = AuthenticationManager()

    def __str__(self):
        return smart_str(self.code)

    class Meta:
        ordering = ['-created_at']


class CorporationUserApplication(models.Model):
    """ 企业用户认证申请记录
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="申请人")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="申请日期")

    license_image = models.ImageField(upload_to=auth_image, verbose_name="营业执照图片")
    id_card_image = models.ImageField(upload_to=auth_image, verbose_name="身份证图片")
    other_info_image = models.ImageField(upload_to=auth_image, verbose_name="补充材料")

    approved = models.BooleanField(default=False, verbose_name="是否已经批准")

    class Meta:
        verbose_name = "企业认证申请"
        verbose_name_plural = "企业认证申请"
        ordering = ("-created_at", )

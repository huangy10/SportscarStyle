# coding=utf-8
import uuid
import hashlib

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import UserManager
from django.utils import timezone
# Create your models here.
from django.utils.encoding import smart_str
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractBaseUser

from custom.utils import time_to_string


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


class User(AbstractBaseUser):
    REQUIRED_FIELDS = ["password", "nick_name"]
    USERNAME_FIELD = "username"

    objects = UserManager()
    # Authentication property
    username = models.CharField(max_length=20, unique=True)
    register_finished = models.BooleanField(default=False)
    # password = models.CharField(max_length=50)

    # Profile information
    nick_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=profile_avatar)
    avatar_club = models.ForeignKey('Club.ClubJoining', null=True, blank=True, related_name="+")
    avatar_car = models.ForeignKey('Sportscar.SportCarOwnership', null=True, blank=True, related_name="+")
    gender = models.CharField(max_length=1, choices=(
        ('m', u'男'),
        ('f', u'女'),
    ), verbose_name=u'性别')
    birth_date = models.DateField(verbose_name=u'出生日期')

    @property
    def age(self):
        current = timezone.now().date()
        d_year = current.year - self.birth_date.year
        if current.month < self.birth_date.month \
                or (current.month == self.birth_date.month and current.day < self.birth_date.day):
            d_year -= 1

        return d_year

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
        ('Aquarius', u'水瓶座'),
        ('Pisces', u'双鱼座'),
    ), verbose_name=u'星座', default='Aries')

    district = models.CharField(max_length=255, verbose_name=u'地区', default='')
    signature = models.CharField(max_length=255, verbose_name=u'签名', default='')
    job = models.CharField(max_length=64, verbose_name='行业', default='')

    # Identification information
    corporation_identified = models.BooleanField(default=False, verbose_name=u"是否是经过认证的企业用户")

    # Statistic data
    fans_num = models.IntegerField(default=0, verbose_name=u"粉丝数量")
    follows_num = models.IntegerField(default=0, verbose_name=u"关注数量")
    status_num = models.IntegerField(default=0, verbose_name=u"动态数量")
    act_num = models.IntegerField(default=0, verbose_name=u"活动数量")
    most_recent_status = models.ForeignKey('Status.Status', blank=True, null=True, related_name='+')

    # User Relations
    follows = models.ManyToManyField(
        "self", through="UserRelation",
        related_name="fans", symmetrical=False
    )

    value = models.IntegerField(default=0, verbose_name=u"拥有的跑车的价值")

    def follow_user(self, user):
        relation, _ = UserRelation.objects.get_or_create(
            source_user=self,
            target_user=user
        )
        return relation

    def follow_cancel(self, user):
        UserRelation.objects.filter(
            source_user=self,
            target_user=user
        ).delete()

    @property
    def friends(self):
        return self.fans.filter(is_friend=True)

    def __str__(self):
        return smart_str(self.nick_name)

    def dict_description(self, detail=False, host=None):
        result = dict(
            ssid=self.id,
            nick_name=self.nick_name,
            avatar=self.avatar.url,
        )
        if self.most_recent_status is not None:
            result.update(recent_status_des=self.most_recent_status.content)
        if not detail:
            return result
        if self.avatar_car is not None:
            result.update(avatar_car=self.avatar_car.dict_description())
        if self.avatar_club is not None:
            result.update(avatar_club=self.avatar_club.dict_description())
        result.update(
            ssid=self.id,
            phone_num=self.username,
            gender=self.get_gender_display(),
            age=self.age,
            star_sign=self.get_star_sign_display(),
            district=self.district,
            signature=self.signature,
            job=self.job,
            corporation_identified=self.corporation_identified,
            follow_num=self.follows_num,
            fans_num=self.fans_num,
            status_num=self.status_num,
        )
        if host is not None and host.id != self.id:
            result.update(followed=UserRelation.objects.filter(source_user=host, target_user=self).exists())
        return result

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.nick_name

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = u"用户"


class UserRelation(models.Model):
    source_user = models.ForeignKey(User, related_name="follows_relation")
    target_user = models.ForeignKey(User, related_name="fans_relation")
    is_friend = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @cached_property
    def reverse_relation(self):
        try:
            reverse_relation = UserRelation.objects.get(
                source_user=self.target_user,
                target_user=self.source_user
            )
            return reverse_relation
        except ObjectDoesNotExist:
            return None

    def dict_description(self, reversed=False):
        result = dict(
            user=self.source_user.dict_description() if reversed else self.target_user.dict_description(),
            created_at=self.created_at,
        )
        return result

    class Meta:
        ordering = ("-created_at", )
        unique_together = ("source_user", "target_user")


@receiver(post_delete, sender=UserRelation)
def auto_maintain_relation(sender, instance, **kwargs):
    source = instance.source_user
    target = instance.target_user
    source.follows_num -= 1
    target.fans_num -= 1
    source.save()
    target.save()
    reverse_relation = instance.reverse_relation
    if reverse_relation is not None:
        reverse_relation.is_friend = False
        reverse_relation.save()


@receiver(post_save, sender=UserRelation)
def auto_maintain_relation_create(sender, instance, created, **kwargs):
    if created:
        source = instance.source_user
        target = instance.target_user
        source.follows_num += 1
        target.fans_num += 1
        source.save()
        target.save()
        reverse_relation = instance.reverse_relation
        if reverse_relation is not None:
            reverse_relation.is_friend = True
            reverse_relation.save()
            instance.is_friend = True
            instance.save()


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


class CorporationAuthenticationRequest(models.Model):

    user = models.ForeignKey(User, verbose_name=u'申请人')
    created_at = models.DateTimeField(auto_now_add=True)

    license_image = models.ImageField(upload_to=auth_image, verbose_name=u'营业执照')
    id_card_image = models.ImageField(upload_to=auth_image, verbose_name=u'身份证图片')
    other_info_image = models.ImageField(upload_to=auth_image, verbose_name=u'补充材料')

    approved = models.BooleanField(default=False, verbose_name=u'是否已经批准')
    revoked = models.BooleanField(default=False, verbose_name=u'申请是否已经驳回')

    class Meta:
        verbose_name = u'企业申请'
        verbose_name_plural = u'企业申请'
        ordering = ("-created_at", )

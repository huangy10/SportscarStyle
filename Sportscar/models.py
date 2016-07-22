# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import smart_str

from Notification.signal import send_notification
from custom.utils import time_to_string

# Create your models here.


def car_logo(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('car_logo', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


def car_image(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('car_image', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


def car_thumbnail(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('car_thumbnail', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


def car_auth_image(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('car_auth_image', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class Manufacturer(models.Model):
    """这个类为对汽车生产商的抽象
    """
    name = models.CharField(max_length=128, verbose_name=u'名称(中文)', unique=True)
    remote_id = models.IntegerField(default=0, unique=True)
    detail_url = models.CharField(max_length=255, verbose_name=u"详情链接")
    logo = models.ImageField(upload_to=car_logo, verbose_name=u"厂商logo")
    logo_remote = models.CharField(max_length=255, verbose_name=u"厂商的logo的url")
    index = models.CharField(max_length=1, verbose_name=u"音序")

    def __str__(self):
        return smart_str(self.name)

    class Meta:
        verbose_name = u'汽车生产商'
        verbose_name_plural = u'汽车生产商'


class Sportscar(models.Model):
    """这个类为对跑车的抽象
    """
    name = models.CharField(max_length=128, verbose_name=u'名称(中文)', unique=True)
    remote_id = models.IntegerField(default=0, verbose_name=u"汽车之家定义的id")

    price = models.CharField(max_length=18, verbose_name=u'价格', default="-")
    price_number = models.IntegerField(default=0, verbose_name=u"价格数值")
    fuel_consumption = models.CharField(max_length=100, default="-", verbose_name=u'油耗', help_text=u'升每百公里')
    engine = models.CharField(max_length=100, verbose_name=u'发动机', default="-")
    transmission = models.CharField(max_length=100, verbose_name=u'变速器', default="-")
    max_speed = models.CharField(max_length=20, verbose_name=u'最高车速', default="-")
    zeroTo60 = models.CharField(max_length=7, verbose_name=u'百公里加速', default="-")
    body = models.CharField(max_length=255, verbose_name=u"车身结构", default="-")
    torque = models.CharField(max_length=255, default=u"-", verbose_name=u'扭矩')

    image = models.ImageField(verbose_name=u'跑车照片', upload_to=car_image)
    thumbnail = models.ImageField(verbose_name=u'缩略图', upload_to=car_thumbnail)
    remote_image = models.CharField(max_length=255, verbose_name=u"远程资源链接", default="")
    remote_thumbnail = models.CharField(max_length=255, verbose_name=u"远程缩略图", default="")

    manufacturer = models.ForeignKey(Manufacturer, verbose_name=u'制造商')
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SportCarOwnership')
    # For the spider to check if the data of this car is fetched
    data_fetched = models.BooleanField(default=False, verbose_name=u"")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.price_number = self.get_price_value(self.price)
        super(Sportscar, self).save(force_insert, force_update, using, update_fields)

    def get_price_value(self, price_str):
        if price_str == "-" or price_str == "":
            return 0
        price_str = price_str.replace(",", "")
        try:
            result = int(price_str)
            return result
        except ValueError:
            if price_str.endswith(u"万"):
                try:
                    result = int(float(price_str[0:-1]) * 10000)
                    return result
                except ValueError:
                    return 0
            return 0

    def __str__(self):
        return smart_str(self.name)

    def dict_description(self):
        return dict(
            name=self.name,
            carID=self.id,
            logo=self.manufacturer.logo.url,
            image=self.image.url,
            thumbnail=self.thumbnail.url,
            price=self.price,
            engine=self.engine,
            trans=self.transmission,
            body=self.body,
            speed=self.max_speed,
            acce=self.zeroTo60,
            torque=self.torque,
        )

    class Meta:
        verbose_name = u'跑车'
        verbose_name_plural = u'跑车'


class SportCarOwnership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ownership')
    car = models.ForeignKey(Sportscar, related_name='ownership')
    signature = models.CharField(max_length=255, verbose_name=u'跑车签名')
    identified = models.BooleanField(default=False, verbose_name=u'是否认证')
    identified_at = models.DateTimeField(blank=True, verbose_name=u'认证日期', null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'拥有日期')

    def dict_description(self):
        return dict(
            car=self.car.dict_description(),
            signature=self.signature,
            identified=self.identified,
            identified_date=time_to_string(self.created_at)
        )

    class Meta:
        verbose_name = u'拥车/关注'
        verbose_name_plural = u'拥车/关注'
        unique_together = ('user', 'car')


class SportCarIdentificationRequestRecord(models.Model):
    """ 跑车认证请求记录
     注意,这里认证的是对跑车的"所有"故这里的待认证对象是Ownership
    """
    ownership = models.ForeignKey(SportCarOwnership, verbose_name=u'待认证跑车')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'申请时间')
    approved = models.BooleanField(default=False, verbose_name=u'是否批准')
    drive_license = models.ImageField(upload_to=car_auth_image, verbose_name=u"驾照")
    id_card = models.ImageField(upload_to=car_auth_image, verbose_name=u'身份证')
    photo = models.ImageField(upload_to=car_auth_image, verbose_name=u"合影")
    license_num = models.CharField(max_length=30, verbose_name=u'车牌号')
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # send_notification.send(
        #     sender=SportCarIdentificationRequestRecord,
        #     target=self.ownership.user,
        #     message_type="auth_car_approved" if self.approved else "auth_car_denied",
        #     related_own=self.ownership,
        #     message_body=""
        # )
        super(SportCarIdentificationRequestRecord, self).save()


@receiver(post_save, sender=SportCarIdentificationRequestRecord)
def auto_update_user_value(sender, instance, created, **kwargs):
    if created:
        return
    old = SportCarIdentificationRequestRecord.objects.get(pk=instance.pk)
    if not old.approved and instance.approved:
        user = instance.ownership.user
        user.value += instance.ownership.car.value_number
        user.save()


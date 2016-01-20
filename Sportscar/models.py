# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

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
    name_english = models.CharField(max_length=128, verbose_name=u'名称(英文)', unique=True)

    class Meta:
        verbose_name = u'汽车生产商'
        verbose_name_plural = u'汽车生产商'


class Sportscar(models.Model):
    """这个类为对跑车的抽象
    """
    name = models.CharField(max_length=128, verbose_name=u'名称(中文)', unique=True)
    name_english = models.CharField(max_length=128, verbose_name=u'名称(英文)', unique=True)
    price = models.CharField(max_length=18, verbose_name=u'价格')
    seats = models.PositiveIntegerField(default=0, verbose_name=u'座位数')
    fuel_consumption = models.FloatField(default=0, verbose_name=u'油耗', help_text=u'升每百公里')
    displacement = models.FloatField(default=0, verbose_name=u'排量', help_text=u'升')
    engine = models.CharField(max_length=100, verbose_name=u'发动机')
    transmission = models.CharField(max_length=100, verbose_name=u'变速器')
    max_speed = models.CharField(max_length=20, verbose_name=u'最高车速')
    zeroTo60 = models.CharField(max_length=7, verbose_name=u'百公里加速')
    release_date = models.DateField(verbose_name=u'发布日期')
    body = models.CharField(max_length=255, verbose_name=u"车身结构")
    logo = models.ImageField(verbose_name=u'车标', upload_to=car_logo)
    image = models.ImageField(verbose_name=u'跑车照片', upload_to=car_image)

    manufacturer = models.ForeignKey(Manufacturer, verbose_name=u'制造商')
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SportCarOwnership')

    def dict_description(self):
        return dict(
            name=self.name,
            carID=self.id,
            logo=self.logo.url,
            image=self.image.url
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
            identified_date=self.created_at.strftime('%Y-%m-%d %H:%M:%S')
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
    images = ArrayField(models.ImageField(upload_to=car_auth_image), size=3, verbose_name=u'认证图片')
    id_card = models.ImageField(upload_to=car_auth_image, verbose_name=u'身份证')
    license_num = models.CharField(max_length=30, verbose_name=u'车牌号')

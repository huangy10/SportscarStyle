# coding=utf-8
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import smart_str

from custom.utils import time_to_string
from User.tasks import user_value_change
from custom.fields import BooleanField

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
    name = models.CharField(max_length=128, verbose_name=u'名称(中文)')
    subname = models.CharField(max_length=128, verbose_name=u'子型号名称', blank=True)
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
    data_fetched = BooleanField(default=False, verbose_name=u"")

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
        result = dict(
            name=self.name,
            subname=self.subname,
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
        medias = self.medias.all()
        media_data = dict(audio=[], image=[], video=[])
        for item in medias:
            media_data[item.item_type].append(item.item_link)
        result.update(medias=media_data)
        return result

    class Meta:
        verbose_name = u'跑车'
        verbose_name_plural = u'跑车'
        unique_together = ("name", "subname")

    def secure_to_delete(self):
        return not SportCarOwnership.objects.filter(car=self).exists()


class SportCarOwnership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ownership')
    car = models.ForeignKey(Sportscar, related_name='ownership')
    signature = models.CharField(max_length=255, verbose_name=u'跑车签名')
    identified = BooleanField(default=False, verbose_name=u'是否认证')
    identified_at = models.DateTimeField(blank=True, verbose_name=u'认证日期', null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'拥有日期')

    def __str__(self):
        return smart_str(
            u"{username}->{car_name}".format(
                username=self.user.username, car_name=self.car.name
            )
        )

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
    approved = BooleanField(default=False, verbose_name=u'是否批准')
    checked = BooleanField(default=False, verbose_name=u'是否已经处理')
    drive_license = models.ImageField(upload_to=car_auth_image, verbose_name=u"驾照")
    id_card = models.ImageField(upload_to=car_auth_image, verbose_name=u'身份证')
    photo = models.ImageField(upload_to=car_auth_image, verbose_name=u"合影")
    license_num = models.CharField(max_length=30, verbose_name=u'车牌号')

    def approve(self):
        if self.checked:
            return
        self.checked = True
        self.approved = True
        own = self.ownership
        own.identified = True
        own.identified_at = timezone.now()
        self.save()

    def deny(self):
        if self.checked:
            return
        self.checked = True
        self.approved = True
        self.save()

    def __str__(self):
        return smart_str(u"{user}->{car}".format(
            user=self.ownership.user.username,
            car=self.ownership.car.name
        ))

    def drive_license_admin(self):
        return '<img src=%s style="max-width:600px"/>' % self.drive_license.url
    drive_license_admin.short_description = u"驾驶执照"
    drive_license_admin.allow_tags = True

    def id_card_admin(self):
        return '<img src=%s style="max-width:600px"/>' % self.id_card.url
    id_card_admin.short_description = u"身份证"
    id_card_admin.allow_tags = True

    def photo_admin(self):
        return '<img src=%s style="max-width:600px"/>' % self.photo.url
    photo_admin.short_description = u"行驶证"
    photo_admin.allow_tags = True

    def link_to_user(self):
        return u'<a href="/admin/User/user/%s">%s(%s)</a>' % (self.ownership.user.id, self.ownership.user.nick_name,
                                                              self.ownership.user.username)
    link_to_user.short_description = u'申请人'
    link_to_user.allow_tags = True

    def link_to_car(self):
        return u'<a href="/admin/Sportscar/sportscar/%s">%s</a>' % (self.ownership.car.id,
                                                                    self.ownership.car.name)
    link_to_car.short_description = u"跑车"
    link_to_car.allow_tags = True

    class Meta:
        verbose_name = u"跑车认证请求"
        verbose_name_plural = u"跑车认证请求"


# @receiver(post_save, sender=SportCarIdentificationRequestRecord)
# def auto_update_user_value(sender, instance, created, **kwargs):
#     if created:
#         return
#     old = SportCarIdentificationRequestRecord.objects.get(pk=instance.pk)
#     if not old.approved and instance.approved:
#         user = instance.ownership.user
#         user.value += instance.ownership.car.value_number
#         user.save()

@receiver(pre_save, sender=SportCarOwnership)
def auto_update_user_value(sender, instance, raw, **kwargs):
    try:
        old_obj = SportCarOwnership.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return
    if old_obj.identified != instance.identified:
        user = instance.user
        user_value_change.delay(user)


@receiver(post_delete, sender=SportCarOwnership)
def auto_update_user_value_after_delete(sender, instance, **kwargs):
    if instance.identified:
        user = instance.user
        user_value_change.delay(user)


@receiver(pre_save, sender=Sportscar)
def auto_update_user_value_after_car_change(sender, instance, raw, **kwargs):
    from User.models import User
    try:
        old_car = Sportscar.objects.get(pk=instance.pk)
    except ObjectDoesNotExist:
        return
    if old_car.price_number != instance.price_number:
        # get related users and recalculate their value
        users = User.objects.filter(ownership__car=instance)
        for user in users:
            user_value_change.delay(user)


MAX_IMAGE_PER_CAR = 50
MAX_VIDEO_PER_CAR = 1
MAX_AUDIO_PER_CAR = 1


class CarMediaItem(models.Model):

    car = models.ForeignKey(Sportscar, verbose_name=u'相关跑车', related_name="medias")
    item = models.FileField(upload_to=car_image, verbose_name=u'关联文件', null=True, blank=True)
    link = models.CharField(max_length=255, verbose_name=u"链接", default="", blank=True,
                            help_text=u"此项不为空时,将覆盖关联文件的内容")
    item_type = models.CharField(max_length=10, choices=(
        ('image', u'图片'), ("video", u'视频'), ('audio', u'音频')
    ))

    order = models.IntegerField(default=0, verbose_name=u'排序权重', help_text=u'从小到大排列')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    @property
    def item_link(self):
        link = self.link
        if link is not None and link != "":
            return link
        else:
            return self.item.url

    def __str__(self):
        return smart_str(u'{car}的{item}'.format(
            car=self.car.name, item=self.get_item_type_display()
        ))

    @classmethod
    def migrate_from_old_version(cls):
        for car in Sportscar.objects.all():
            CarMediaItem.objects.create(car=car, item_type="image", item=car.image.name)

    class Meta:
        ordering = ('order', 'created_at')


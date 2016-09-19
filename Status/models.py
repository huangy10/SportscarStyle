# coding=utf-8
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from Sportscar.models import SportCarOwnership
from custom.models_template import BaseCommentManager, comment_image_path
from custom.utils import time_to_string
# Create your models here.


def status_image_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('cover_path', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class Status(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # 由于Django的ArrayField只能应用到的PostgreSQL使用,由于将来可能会更换数据库,这里不适用ArrayField而是将其拆分成为9个ImageField
    image1 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image2 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image3 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image4 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image5 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image6 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image7 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image8 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)
    image9 = models.ImageField(upload_to=status_image_path, verbose_name=u'状态图', null=True, blank=True)

    content = models.CharField(max_length=255, verbose_name=u'正文', default="", blank=True)
    location = models.ForeignKey('Location.Location', verbose_name=u'发布地点', null=True, blank=True)
    car = models.ForeignKey('Sportscar.Sportscar', verbose_name=u'签名跑车', null=True, blank=True)

    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'点赞', related_name='liked_status',
                                      through='StatusLikeThrough')
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'提醒谁看',
                                       related_name='status_need_to_see')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'发布日期')
    #
    deleted = models.BooleanField(default=False, verbose_name=u"是否已经被删除")

    class Meta:
        verbose_name = u'状态'
        verbose_name_plural = u'状态'

    def as_recent_des(self):
        if self.content == "":
            return u"[图片]"
        else:
            return self.content

    @property
    def images(self):
        """ 将所有非空的image的url整理成一个字符串,以分号分隔
        """
        images_url = []
        for i in range(1, 10):
            image = getattr(self, "image%s" % i)
            if image:
                images_url.append(image.url)
        return ";".join(images_url)

    def dict_description(self, show_liked=False, user=None):
        """ 获取字典形式的数据描述,字典形式的注释参见view.py中的status_list的注释
         但是这里没有生成comment_num和like_num这两个字段
        """
        result = dict(
            statusID=self.id,
            images=self.images,
            content=self.content,
            user=self.user.dict_description(detail=True),
            created_at=time_to_string(self.created_at)
        )
        if self.car is not None:
            try:
                own = SportCarOwnership.objects.get(user=self.user, car=self.car)
                result["car"] = own.dict_description()
            except ObjectDoesNotExist:
                result["car"] = self.car.dict_description()
        if self.location is not None:
            result["location"] = self.location.dict_description()
        if hasattr(self, "comment_num"):
            result["comment_num"] = self.comment_num
        if hasattr(self, "like_num"):
            result["like_num"] = self.like_num
        if show_liked:
            result["liked"] = StatusLikeThrough.objects.filter(status=self, user=user).exists()
        return result


class StatusComment(models.Model):

    status = models.ForeignKey(Status, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'发布用户', related_name='+')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间', blank=True)
    image = models.ImageField(upload_to=comment_image_path, verbose_name=u'评论图片')
    content = models.CharField(max_length=255, verbose_name=u'评论正文', null=True, blank=True)
    response_to = models.ForeignKey('self', related_name='responses', null=True, blank=True)
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'@某人',
                                       related_name='status_comments_need_to_see')
    objects = BaseCommentManager()

    class Meta:
        abstract = False
        verbose_name = u'状态评论'
        verbose_name_plural = u'状态评论'

    def dict_description(self):
        result = dict(
            user=self.user.dict_description(),
            created_at=time_to_string(self.created_at),
            image=self.image.url if self.image else None,
            content=self.content,
            commentID=self.id
        )
        if self.response_to is not None:
            result.update(response_to=self.response_to.dict_description())
        return result

    # def dict_description(self):
    #     return dict(
    #         commentID=self.id,
    #         created_at=time_to_string(self.created_at),
    #         image=self.image.url if self.image else "",
    #         content=self.content,
    #         user=self.user.dict_description(),
    #         response_to=self.response_to_id
    #     )


class StatusLikeThrough(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.ForeignKey(Status)
    like_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'status')


@receiver(post_save, sender=Status)
def auto_set_most_recent_status(sender, instance, created, **kwargs):
    if not created:
        return
    instance.user.most_recent_status = instance
    instance.user.status_num += 1
    instance.user.save()


class StatusReport(models.Model):
    """
     对动态的举报
    """
    status = models.ForeignKey(Status)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    reason = models.CharField(max_length=255)
    checked = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"举报信息"
        verbose_name_plural = u'举报信息'

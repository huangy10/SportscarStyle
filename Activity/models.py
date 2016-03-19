# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from custom.models_template import comment_image_path, BaseCommentManager
from custom.utils import time_to_string

# Create your models here.


def activity_poster(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".format(
            'activity_poster',
            current.year,
            current.month,
            current.day,
            random_file_name,
            ext
    )
    return new_file_name


class Activity(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'活动名称')
    description = models.TextField(verbose_name=u'活动描述')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"活动发起者")

    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u'通知谁看',
                                       related_name='activities_need_to_see')
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u"喜欢这个活动的人",
                                      related_name="liked_acts")
    max_attend = models.PositiveIntegerField(default=0, verbose_name=u'人数上限')
    start_at = models.DateTimeField(verbose_name=u'开始时间')
    end_at = models.DateTimeField(verbose_name=u'结束时间')
    allowed_club = models.ForeignKey('Club.Club', verbose_name=u'允许加入的俱乐部', blank=True, null=True)
    poster = models.ImageField(upload_to=activity_poster, verbose_name=u'活动海报')
    location = models.ForeignKey('Location.Location', verbose_name=u'活动地点')

    closed = models.BooleanField(default=False, verbose_name="活动报名是否关闭")
    closed_at = models.DateTimeField(default=timezone.now, verbose_name="关闭报名的时间")

    appliers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      through="ActivityJoin", verbose_name="申请者", related_name="applied_acts")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'活动'
        verbose_name_plural = u'活动'
        ordering = ("-created_at",)

    def dict_description_without_user(self):
        result = dict(
                actID=self.id,
                name=self.name,
                description=self.description,
                max_attend=self.max_attend,
                start_at=time_to_string(self.start_at),
                end_at=time_to_string(self.end_at) if not self.closed \
                    else time_to_string(self.closed_at),
                poster=self.poster.url,
                location=self.location.dict_description(),
                created_at=time_to_string(self.created_at),
        )
        if self.allowed_club is not None:
            result.update(allowed_club=self.allowed_club.dict_description())
        return result

    def dict_description_with_aggregation(self, with_user_info=False, show_members=False):
        """ 获取对象的字典表示形式方便json化
         :param with_user_info  是否携带活动发布者的信息
         :param show_members    显示参与者信息
        """
        if with_user_info:
            result = self.dict_description()
        else:
            result = self.dict_description_without_user()
        result["like_num"] = self.like_num
        result["comment_num"] = self.comment_num
        if show_members:
            result["members"] = map(lambda x: x.profile.simple_dict_description(), self.applications.all())
        return result

    def dict_description(self):
        result = dict(
                actID=self.id,
                name=self.name,
                description=self.description,
                max_attend=self.max_attend,
                start_at=time_to_string(self.start_at),
                end_at=time_to_string(self.end_at) if not self.closed \
                    else time_to_string(self.closed_at),
                poster=self.poster.url,
                location=self.location.dict_description(),
                created_at=time_to_string(self.created_at),
                user=self.user.profile.simple_dict_description()
        )
        if self.allowed_club is not None:
            result.update(allowed_club=self.allowed_club.dict_description())
        return result


class ActivityJoin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="applications")
    activity = models.ForeignKey(Activity, related_name="applications")
    approved = models.BooleanField(default=True)  # 不需要审核,这里总为true
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def dict_description(self):
        return dict(
                user=self.user.profile.simple_dict_description(),
                activity=self.activity.dict_description(),
                approved=self.approved,
                created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S %Z')
        )


class ActivityLikeThrough(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户")
    activity = models.ForeignKey(Activity, verbose_name="活动")
    create_at = models.DateTimeField(auto_now_add=True)


class ActivityComment(models.Model):
    activity = models.ForeignKey(Activity, verbose_name='相关活动', related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=comment_image_path, verbose_name='评论图片')
    content = models.CharField(max_length=255, verbose_name='评论正文')
    response_to = models.ForeignKey('self', related_name='responses', null=True, blank=True)
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='@某人',
                                       related_name='activity_comments_need_to_see')

    objects = BaseCommentManager()

    class Meta:
        verbose_name = '活动评论'
        verbose_name_plural = '活动评论内容'

    def dict_description(self):
        result = dict(
                activity=self.activity.dict_description(),
                user=self.user.profile.simple_dict_description(),
                created_at=time_to_string(self.created_at),
                image=self.image.url if self.image else None,
                content=self.content,
                commentID=self.id
        )
        if self.response_to is not None:
            result.update(response_to=self.response_to_id)
        return result

    def dict_description_simple(self):
        """ 相比之下,这个函数返回的字典不包含activity的信息
        """
        result = dict(
                user=self.user.profile.simple_dict_description(),
                created_at=time_to_string(self.created_at),
                image=self.image.url if self.image else None,
                content=self.content,
                commentID=self.id
        )
        if self.response_to is not None:
            result.update(response_to=self.response_to_id)
        return result


class ActivityInvitation(models.Model):
    """ 活动邀请
    """
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL)
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="invites")
    activity = models.ForeignKey(Activity)
    created_at = models.DateTimeField(auto_now_add=True)
    responsed = models.BooleanField(default=False)  # 被邀请者是否已经回应了这个邀请
    agree = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "活动邀请"
        verbose_name = "活动邀请"
        ordering = ("-created_at",)

    def dict_description(self):
        return dict(
                inviter=self.inviter.profile.simple_dict_description(),
                target=self.target.profile.simple_dict_description(),
                activity=self.target.dict_description(),
                created_at=time_to_string(self.created_at),
                responsed=self.responsed,
                agree=self.agree
        )

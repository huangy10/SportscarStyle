# coding=utf-8
import urllib

from django.db import models
from django.conf import settings
from django.dispatch import receiver

from custom.utils import time_to_string
from .tasks import push_notification
from .signal import send_notification
from tornado.httpclient import HTTPClient
# from Chat.ChatServer.runner import _dispatcher as dispatcher
# Create your models here.


class Notification(models.Model):

    target = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="目标用户")
    message_type = models.CharField(max_length=100, choices=(
        ("status_like", "status_like"),
        ("status_comment", "your_status_are_commmented_by_others"),
        ("status_comment_replied", "your_comment_on_a_status_is_responsed_by_others"),
        ("status_inform", ""),
        ("news_comment_replied", "your commemnt_on_a_news_is_responsed_by_others"),
        ("act_applied", "some_one_applys_your_activity"),
        ("act_approved", "your_application_on_an_activity_is_approved"),
        ("act_denied", "your_application_on_an_activity_is_denied"),
        ("act_full", "one_of_your_activity_if_full_off_applicators"),
        ("act_deleted", "one_of_your_applied_activity_is_deleted"),
        ("act_application_cancel", "one_application_is_cancelled"),
        ("act_invited", "some_one_invite_you_for_an_activity"),
        ("act_invitation_agreed", "your_invitation_is_agreed"),
        ("act_invitation_denied", "your_invitation_is_denied"),
        ("act_comment", ""),
        ("act_comment_replied", ""),
        ("auth_car_approved", "your_application_for_sportscar_identification_is_approved"),
        ("auth_car_denied", "your_application_for_sportscar_identification_is_denied"),
        ("auth_club_approved", "your_application_for_club_identification_is_approved"),
        ("auth_club_denied", "your_application_for_club_identification_is_denied"),
        ("auth_act_approved", ""),
        ("auth_act_denied", ""),
        ("relation_follow", ""),
        ("chat", ""),
        ("club_apply", ""),
    ))
    related_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+", null=True)
    related_act = models.ForeignKey("Activity.Activity", related_name="+", null=True)
    related_act_invite = models.ForeignKey("Activity.ActivityInvitation", related_name="+", null=True)
    related_act_comment = models.ForeignKey("Activity.ActivityComment", related_name="+", null=True)
    related_act_join = models.ForeignKey("Activity.ActivityJoin", related_name="+", null=True)
    related_club = models.ForeignKey("Club.Club", related_name="+", null=True)
    related_status = models.ForeignKey("Status.Status", related_name="+", null=True)
    related_status_comment = models.ForeignKey("Status.StatusComment", related_name="+", null=True)
    related_news = models.ForeignKey("News.News", related_name="+", null=True)
    related_news_comment = models.ForeignKey("News.NewsComment", related_name="+", null=True)
    related_own = models.ForeignKey("Sportscar.SportCarOwnership", related_name="+", null=True)

    message_body = models.CharField(max_length=255, verbose_name="消息内容(Optional)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    read = models.BooleanField(default=False, verbose_name="是否已读")
    flag = models.BooleanField(default=False, verbose_name="保留字段")      # 额外供特殊消息类型使用的字段
    checked = models.BooleanField(default=False, verbose_name="是否已经操作")

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "消息"
        verbose_name_plural = "消息"

    def dict_description(self):
        """ 获取字典表示形式
        """
        result = dict(
            notification_id=self.id,
            target=self.target.dict_description(),
            message_type=self.message_type,
            read=self.read,
            created_at=time_to_string(self.created_at),
            flag=self.flag,
            checked=self.checked
        )

        def set_related(attribute_name):
            attribute = getattr(self, attribute_name)
            if attribute is not None:
                result[attribute_name] = attribute.dict_description()
            # if attribute is not None:
            #     if attribute_name == "related_user":
            #         result[attribute_name] = attribute.profile.simple_dict_description()
            #     else:

        set_related("related_user")
        set_related("related_act")
        set_related("related_act_invite")
        set_related("related_act_join")
        set_related("related_act_comment")
        set_related("related_club")
        set_related("related_status")
        set_related("related_status_comment")
        set_related("related_news")
        set_related("related_news_comment")
        set_related("related_own")

        return result

    def apns_des(self):
        if self.message_type == "status_like":
            return "{0} 赞了你的动态".format(self.related_user.nick_name)
        elif self.message_type == "status_comment":
            return "{0} 评论了你的动态".format(self.related_user.nick_name)
        elif self.message_type == "relation_follow":
            return "{} 关注了你".format(self.related_user.nick_name)
        return u"未定义的消息"


@receiver(send_notification)
def send_notification_handler(sender, **kwargs):
    message_type = kwargs["message_type"]
    target = kwargs["target"]
    message_body = kwargs.get("message_body", None)

    create_params = dict(
        message_type=message_type,
        target=target, message_body=message_body,
        related_user=kwargs.get("related_user", None),
        related_act=kwargs.get("related_act", None),
        related_act_invite=kwargs.get("related_act_invite", None),
        related_act_join=kwargs.get("related_act_join", None),
        related_act_comment=kwargs.get("related_act_join", None),
        related_club=kwargs.get("related_club", None),
        related_status=kwargs.get("related_status", None),
        related_status_comment=kwargs.get("related_status_comment", None),
        related_news=kwargs.get("related_news", None),
        related_news_comment=kwargs.get("related_news_commnet", None),
        related_own=kwargs.get("related_own", None)
    )
    print "send notification"
    notif = Notification.objects.create(**create_params)
    client = HTTPClient()
    response = client.fetch(
        "http://localhost:8887/notification/internal", method="POST",
        body=urllib.urlencode({"id": notif.id})
    )
    # tokens = RegisteredDevices.objects.filter(
    #     user=notif.target, is_active=True
    # ).values_list("token", flat=True)
    # print "push"
    # push_notification.delay(target, tokens, badge_incr=1, message_body=notif.apns_des(), type="notif")


class RegisteredDevices(models.Model):
    token = models.CharField(max_length=255, verbose_name=u"推送使用的token", null=True, blank=True)
    device_id = models.CharField(max_length=255, verbose_name=u"设备的id")
    device_type = models.CharField(max_length=50, default='ios')
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="devices")
    is_active = models.BooleanField(default=True)
    # save badge_number in the redis database, the key is the device_t
    # badge_number = models.IntegerField(default=0)


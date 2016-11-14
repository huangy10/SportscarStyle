# coding=utf-8
import urllib

from django.db import models
from django.conf import settings
from django.dispatch import receiver

from Club.models import Club
from custom.utils import time_to_string, get_logger
from .signal import send_notification
from .tasks import send_notification_handler
from custom.fields import BooleanField
# from Chat.ChatServer.runner import _dispatcher as dispatcher
# Create your models here.


logger = get_logger(__name__)


class Notification(models.Model):

    target = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="目标用户")
    # 消息类型定义如下: 消息类型为由横杠连接的两个部分,前一个部分是关联类的名字,后一个部分前端显示的分类标识
    display_mode = models.CharField(max_length=20, choices=(
        ("minimal", "minimal"), ("with_cover", "with_cover"), ("interact", "interact")
    ))
    extra_info = models.CharField(max_length=20)
    sender_class_name = models.CharField(max_length=50)
    message_type_backup = models.CharField(max_length=100, default="")
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

    # message_body = models.CharField(max_length=255, verbose_name="消息内容(Optional)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    read = BooleanField(default=False, verbose_name="是否已读")
    flag = BooleanField(default=False, verbose_name="保留字段")      # 额外供特殊消息类型使用的字段
    checked = BooleanField(default=False, verbose_name="是否已经操作")

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
                if isinstance(attribute, Club):
                    result[attribute_name] = attribute.dict_description(
                        show_attended=True, target_user=self.target
                    )
                else:
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

    @property
    def message_type(self):
        result = "{display_mode}:{sender}".format(sender=self.sender_class_name, display_mode=self.display_mode)
        if self.extra_info != "":
            result += ":%s" % self.extra_info
        return result

    def apns_des(self):
        element = self.message_type.split(":")
        if len(element) < 1:
            return u"未定义的消息"
        message_type = ":".join(element[1:])
        if message_type == "Status:like":
            return "{0} 赞了你的动态".format(self.related_user.nick_name)
        elif message_type == "StatusComment:response":
            return "{0} 在动态中回复了你".format(self.related_user.nick_name)
        elif message_type == "User:like":
            return "{0} 关注了你".format(self.related_user.nick_name)
        elif message_type == "ActivityJoin:invited":
            return "{0} 邀请你参加活动".format(self.related_user.nick_name)
        elif message_type == "ActivityJoin:invite_agreed":
            return "{0} 接受了你的活动邀请".format(self.related_user.nick_name)
        elif message_type == "ActivityJoin:invite_denied":
            return "{0} 拒绝了你的活动邀请".format(self.related_user.nick_name)
        elif message_type == "ActivityJoin:kick_out":
            return "{0} 将你请出了活动".format(self.related_user.nick_name)
        elif message_type == "Activity:like":
            return "{0} 赞了你的活动".format(self.related_user.nick_name)
        elif message_type == "ActivityJoin:apply":
            return "{0} 报名了你的活动".format(self.related_user.nick_name)
        elif message_type == "ClubJoining:apply":
            return "{0} 申请加入你的俱乐部".format(self.related_user.nick_name)
        elif message_type == "ClubJoining:agree":
            return "{0} 俱乐部的所有者同意了你的申请".format(self.related_club.name)
        elif message_type == "ClubJoining:deny":
            return "{0} 俱乐部的所有者拒绝了你的申请".format(self.related_club.name)
        elif message_type == "ActivityComment:response":
            return "{0} 在活动中回复了你".format(self.related_user.nick_name)
        return u"未定义的消息"


@receiver(send_notification)
def send_notification_message_handler(sender, **kwargs):
    kwargs["signal"] = None
    send_notification_handler.delay(sender, **kwargs)
    # message_type = kwargs["message_type"]
    # target = kwargs["target"]
    # message_body = kwargs.get("message_body", None)
    #
    # create_params = dict(
    #     message_type=message_type,
    #     target=target, message_body=message_body,
    #     related_user=kwargs.get("related_user", None),
    #     related_act=kwargs.get("related_act", None),
    #     related_act_invite=kwargs.get("related_act_invite", None),
    #     related_act_join=kwargs.get("related_act_join", None),
    #     related_act_comment=kwargs.get("related_act_join", None),
    #     related_club=kwargs.get("related_club", None),
    #     related_status=kwargs.get("related_status", None),
    #     related_status_comment=kwargs.get("related_status_comment", None),
    #     related_news=kwargs.get("related_news", None),
    #     related_news_comment=kwargs.get("related_news_commnet", None),
    #     related_own=kwargs.get("related_own", None)
    # )
    #
    # try:
    #     notif, _ = Notification.objects.get_or_create(**create_params)
    # except Exception, e:
    #     logger.error(u'-------->Fail to create Notification')
    #     logger.error(u'the error info is %s' % e)
    #     logger.error(u'message type is %s' % message_type)
    #     # re-throw the exception, let it crash
    #     raise e
    # client = HTTPClient()
    # response = client.fetch(
    #     "http://localhost:8887/notification/internal", method="POST",
    #     body=urllib.urlencode({"id": notif.id})
    # )
    #
    # client.close()
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
    is_active = BooleanField(default=True)
    # save badge_number in the redis database, the key is the device_t
    # badge_number = models.IntegerField(default=0)


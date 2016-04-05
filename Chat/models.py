# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from Club.models import ClubJoining
from custom.utils import time_to_string

# Create your models here.


def chat_image_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('chat_files', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class ChatRecordBasic(models.Model):

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)

    chat_type = models.CharField(max_length=10, choices=(
        ("private", "private"),
        ("group", "group"),
    ))
    # 若chat_type是private,则这是目标用户的id,否则是Club的id
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="目标用户", null=True, blank=True,
                                    related_name="chats_to_me")
    target_club = models.ForeignKey("Club.Club", verbose_name="目标群聊", null=True, blank=True, related_name="chats")

    @cached_property
    def target_club_joing(self):
        if self.chat_type == "private":
            return None
        else:
            return ClubJoining.objects.get(club=self.target_club, user=self.sender)

    # 用来唯一确定一个聊天对象的identifier,其组成方式是:
    # 当聊天类型是group时,这个标识符为目标club的id
    # 当聊天类型是private时,这个标识符为以下划线链接的sender和target_user的组合,这两个id小的在前,大的在后
    distinct_identifier = models.CharField(max_length=20)

    @property
    def target_id(self):
        if self.chat_type == "private":
            return self.target_user_id
        else:
            return self.target_club_id

    message_type = models.CharField(max_length=15, choices=(
        ("text", "text"),
        ("image", "image"),
        ("audio", "audio"),
        ("activity", "activity"),
        ("share", "share"),
        ("contact", "contact"),
        ("placeholder", "placeholder"),
    ))
    image = models.ImageField(upload_to=chat_image_path, verbose_name="相关图片", null=True, blank=True)
    text_content = models.CharField(max_length=255, verbose_name="文字内容", null=True, blank=True)
    audio = models.FileField(upload_to=chat_image_path, verbose_name="相关音频", null=True, blank=True)
    related_id = models.IntegerField(default=0, verbose_name="相关绑定id")      # 对于活动消息而言这里存储的是对应活动的id

    deleted = models.BooleanField(default=False, verbose_name="是否已经被删除")

    # 未读消息数量统计策略如下:
    # 1. 对于private类型的聊天而言,直接通过这个read属性来统计
    # 2. 对于group类型而言,通过标注ClubJoining中的chat_sync_date属性来区分已读和未读的消息数量
    read = models.BooleanField(default=False, verbose_name="是否已读")

    def message_body_des(self):
        if self.message_type == "text":
            content = self.text_content
        elif self.message_type == "audio":
            content = "[语音]"
        else:
            content = "[图片]"
        return "{0}: {1}".format(self.sender.profile.nick_name, content)

    def dict_description(self):
        result = dict(
            chatID=self.id,
            sender=self.sender.profile.simple_dict_description(),
            chat_type=self.chat_type,
            target_id=self.target_id,
            message_type=self.message_type,
            image=self.image.url if self.image else None,
            image_width=self.image.width if self.image else 0,
            image_height=self.image.height if self.image else 0,
            text_content=self.text_content,
            audio=self.audio.url if self.audio else None,
            related_id=self.related_id,
            created_at=time_to_string(self.created_at),
            read=self.read,
            distinct_identifier=self.distinct_identifier
        )
        if self.chat_type == "private":
            result["target_user"] = self.target_user.profile.simple_dict_description()
        else:
            result["target_club"] = self.target_club.dict_description()
        return result

    class Meta:
        ordering = ("distinct_identifier", "-created_at")


@receiver(pre_save, sender=ChatRecordBasic)
def auto_create_distince_identifier(sender, instance, **kwargs):

    if instance.chat_type == "private":
        sender_id = instance.sender.id
        target_id = instance.target_user.id
        if sender_id < target_id:
            instance.distinct_identifier = "{0}_{1}".format(sender_id, target_id)
        else:
            instance.distinct_identifier = "{0}_{1}".format(target_id, sender_id)
    else:
        instance.distinct_identifier = str(instance.target_club.id)

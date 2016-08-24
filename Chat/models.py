# coding=utf-8
import uuid
import json
import librosa
import numpy as np
from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils.functional import cached_property

from Club.models import ClubJoining
from custom.utils import time_to_string
from .utils import ChatRemarkNameStorage

# Create your models here.


def chat_image_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('chat_files', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


# class ChatRecordBasic(models.Model):
#
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chats")
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     chat_type = models.CharField(max_length=10, choices=(
#         ("private", "private"),
#         ("group", "group"),
#     ))
#     # 若chat_type是private,则这是目标用户的id,否则是Club的id
#     target_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="目标用户", null=True, blank=True,
#                                     related_name="chats_to_me")
#     target_club = models.ForeignKey("Club.Club", verbose_name="目标群聊", null=True, blank=True, related_name="chats")
#
#     @cached_property
#     def target_club_joing(self):
#         if self.chat_type == "private":
#             return None
#         else:
#             return ClubJoining.objects.get(club=self.target_club, user=self.sender)
#
#     # 用来唯一确定一个聊天对象的identifier,其组成方式是:
#     # 当聊天类型是group时,这个标识符为目标club的id
#     # 当聊天类型是private时,这个标识符为以下划线链接的sender和target_user的组合,这两个id小的在前,大的在后
#     distinct_identifier = models.CharField(max_length=20)
#
#     @property
#     def target_id(self):
#         if self.chat_type == "private":
#             return self.target_user_id
#         else:
#             return self.target_club_id
#
#     message_type = models.CharField(max_length=15, choices=(
#         ("text", "text"),
#         ("image", "image"),
#         ("audio", "audio"),
#         ("activity", "activity"),
#         ("share", "share"),
#         ("contact", "contact"),
#         ("placeholder", "placeholder"),
#     ))
#     image = models.ImageField(upload_to=chat_image_path, verbose_name="相关图片", null=True, blank=True)
#     text_content = models.CharField(max_length=255, verbose_name="文字内容", null=True, blank=True)
#     audio = models.FileField(upload_to=chat_image_path, verbose_name="相关音频", null=True, blank=True)
#     related_id = models.IntegerField(default=0, verbose_name="相关绑定id")      # 对于活动消息而言这里存储的是对应活动的id
#
#     deleted = models.BooleanField(default=False, verbose_name="是否已经被删除")
#
#     # 未读消息数量统计策略如下:
#     # 1. 对于private类型的聊天而言,直接通过这个read属性来统计
#     # 2. 对于group类型而言,通过标注ClubJoining中的chat_sync_date属性来区分已读和未读的消息数量
#     read = models.BooleanField(default=False, verbose_name="是否已读")
#
#     def message_body_des(self):
#         if self.message_type == "text":
#             content = self.text_content
#         elif self.message_type == "audio":
#             content = u"[语音]"
#         else:
#             content = u"[图片]"
#         return u"{0}: {1}".format(self.sender.profile.nick_name, content)
#
#     def dict_description(self):
#         result = dict(
#             chatID=self.id,
#             sender=self.sender.dict_description(),
#             chat_type=self.chat_type,
#             target_id=self.target_id,
#             message_type=self.message_type,
#             image=self.image.url if self.image else None,
#             image_width=self.image.width if self.image else 0,
#             image_height=self.image.height if self.image else 0,
#             text_content=self.text_content,
#             audio=self.audio.url if self.audio else None,
#             related_id=self.related_id,
#             created_at=time_to_string(self.created_at),
#             read=self.read,
#             distinct_identifier=self.distinct_identifier
#         )
#         if self.chat_type == "private":
#             result["target_user"] = self.target_user.dict_description()
#         else:
#             result["target_club"] = self.target_club.dict_description()
#         return result
#
#     class Meta:
#         ordering = ("distinct_identifier", "-created_at")


# @receiver(pre_save, sender=ChatRecordBasic)
# def auto_create_distince_identifier(sender, instance, **kwargs):
#
#     if instance.chat_type == "private":
#         sender_id = instance.sender.id
#         target_id = instance.target_user.id
#         if sender_id < target_id:
#             instance.distinct_identifier = "{0}_{1}".format(sender_id, target_id)
#         else:
#             instance.distinct_identifier = "{0}_{1}".format(target_id, sender_id)
#     else:
#         instance.distinct_identifier = str(instance.target_club.id)


class ChatEntity(models.Model):
    # 聊天列表的项目, 顺便关于聊天的诸多设置也都可以放在这里
    user = models.ForeignKey('User.User', related_name='+', verbose_name=u'关联的用户', null=True, blank=True)
    club = models.ForeignKey('Club.Club', related_name='+', verbose_name=u'关联的群聊', null=True, blank=True)
    host = models.ForeignKey('User.User', related_name='rosters', verbose_name=u'所有者')
    # nick_name = models.CharField(max_length=255, verbose_name=u'备注名称')
    unread_num = models.IntegerField(default=0, verbose_name=u'未读消息数量')
    recent_chat = models.CharField(max_length=255, verbose_name=u"最近一条聊天的内容")

    # settings
    always_on_top = models.BooleanField(default=False, verbose_name=u'聊天置顶')
    no_disturbing = models.BooleanField(default=False, verbose_name=u'消息免打扰')

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_nick_name(self, name):
        if self.user is None:
            return
        ChatRemarkNameStorage.set_nick_name(self.host, self.user, name=name)

    def dict_description(self):
        result = dict(
            ssid=self.id,
            unread_num=self.unread_num,
            recent_chat=self.recent_chat,
            always_on_top=self.always_on_top,
            no_disturbing=self.no_disturbing,
            created_at=time_to_string(self.created_at),
            updated_at=time_to_string(self.updated_at),
        )
        if self.user is not None:
            user_json = self.user.dict_description()
            user_json.update(note_name=ChatRemarkNameStorage.get_nick_name(self.host, self.user))
            result.update(
                user=user_json,
                entity_type="user"
            )
        if self.club is not None:
            result.update(
                club=self.club.dict_description(show_members_num=True),
                entity_type='club'
            )
        return result

    class Meta:
        ordering = ('-updated_at', )
        verbose_name = u'花名册项'
        verbose_name_plural = u'花名册项'
        unique_together = ('user', 'host')


class Chat(models.Model):

    sender = models.ForeignKey('User.User', related_name='chats')
    chat_type = models.CharField(max_length=10, choices=(
        ('user', 'user'),
        ('club', 'club')
    ))

    target_user = models.ForeignKey('User.User', null=True, blank=True, related_name='chats_to_me')
    target_club = models.ForeignKey('Club.Club', null=True, blank=True, related_name='chats')

    message_type = models.CharField(max_length=15, choices=(
        ("text", "text"),
        ("image", "image"),
        ("audio", "audio"),
        ("placeholder", "placeholder"),
    ))

    image = models.ImageField(upload_to=chat_image_path, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    audio = models.FileField(upload_to=chat_image_path, null=True, blank=True)

    audio_wave_data = models.CharField(max_length=2000, default="")
    audio_length = models.FloatField(default=0, verbose_name=u'音频文件的长度')

    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def message_body_des(self):
        if self.message_type == "text":
            content = self.text
        elif self.message_type == "audio":
            content = u"[语音]"
        else:
            content = u"[图片]"

        if self.chat_type == "user":
            nick_name = ChatRemarkNameStorage.get_nick_name(self.target_user, self.sender)
        else:
            nick_name = self.sender.nick_name
        return u"{0}: {1}".format(nick_name, content)

    @property
    def message_content_des(self):
        if self.chat_type == "club":
            return self.message_body_des
        if self.message_type == "text":
            content = self.text
        elif self.message_type == "audio":
            content = u"[语音]"
        else:
            content = u"[图片]"
        return content

    def dict_description(self, host):
        """
        :param host:
        :return:
        """
        if isinstance(host, ChatEntity):
            host = host.user
        data = self.sender.dict_description()
        data.update(note_name=ChatRemarkNameStorage.get_nick_name(host, self.sender))
        result = dict(
            chatID=self.id,
            sender=data,
            chat_type=self.chat_type,
            message_type=self.message_type,
            created_at=time_to_string(self.created_at)
        )
        if self.image is not None and self.image:
            result.update(
                image=self.image.url,
                image_width=self.image.width,
                image_height=self.image.height
            )
        if self.text is not None:
            result.update(text=self.text)
        if self.audio is not None and self.audio:
            result.update(
                audio=self.audio.url,
                audio_wave_data=self.audio_wave_data,
                audio_length=self.audio_length
            )
        if self.target_user is not None:
            data = self.target_user.dict_description()
            data.update(note_name=ChatRemarkNameStorage.get_nick_name(host, self.target_user))
            result.update(
                target_user=data
            )
        if self.target_club is not None:
            result.update(
                target_club=self.target_club.dict_description()
            )
        return result

    class Meta:
        ordering = ("-created_at", )


@receiver(post_save, sender=Chat)
def auto_set_recent_chat(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.chat_type == "club":
        ChatEntity.objects.filter(club=instance.target_club).update(recent_chat=instance.message_body_des)
    else:
        ChatEntity.objects.filter(
            Q(host=instance.sender, user=instance.target_user) |
            Q(host=instance.target_user, user=instance.sender))\
            .update(recent_chat=instance.message_content_des)


@receiver(post_save, sender=Chat)
def auto_create_audio_wav_data(sender, instance, created, **kwargs):
    if created and instance.message_type == "audio":
        y, sr = librosa.load(instance.audio.path)
        instance.audio_length = librosa.core.get_duration(y=y, sr=sr)

        y = librosa.util.frame(np.abs(y), frame_length=30)
        y = map(lambda x: float(np.max(x)), y)
        instance.audio_wave_data = json.dumps(y)
        instance.save()


@receiver(post_delete, sender=ClubJoining)
def auto_delete_chat_after_club_quit(sender, instance, **kwargs):
    try:
        chat = ChatEntity.objects.get(host=instance.user, club=instance.club)
        chat.delete()
    except ObjectDoesNotExist:
        pass



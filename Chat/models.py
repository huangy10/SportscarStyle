# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


def chat_image_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('chat_files', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    club = models.ForeignKey('Club.Club', verbose_name=u'发生的群聊')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'发布时间')

    content = models.CharField(max_length=255, verbose_name=u'正文内容')
    image = models.ImageField(upload_to=chat_image_path, verbose_name=u'聊天图片', help_text=u'一次一张')
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_need_to_read', verbose_name=u'@')

    class Meta:
        verbose_name = u'聊天记录'
        verbose_name_plural = u'聊天记录'
        ordering = ['-created_at']


class ChatRecordBasic(models.Model):

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)

    chat_type = models.CharField(max_length=10, choices=(
        ("private", "private"),
        ("group", "group"),
    ))
    # 若chat_type是private,则这是目标用户的id,否则是Club的id
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="目标用户", null=True, blank=True)
    target_club = models.ForeignKey("Club.Club", verbose_name="目标群聊", null=True, blank=True)

    # 用来唯一确定一个聊天对象的identifier,其组成方式是(target_id)_(chat_type)
    distinct_identifier = models.CharField(max_length=20)

    @property
    def target_id(self):
        if self.chat_type == "private":
            return self.target_user_id
        else:
            return self.target_club_id

    message_type = models.CharField(max_length=10, choices=(
        ("text", "text"),
        ("image", "image"),
        ("audio", "audio"),
        ("activity", "activity"),
        ("share", "share"),
        ("contact", "contact")
    ))
    image = models.ImageField(upload_to=chat_image_path, verbose_name="相关图片", null=True, blank=True)
    text_content = models.CharField(max_length=255, verbose_name="文字内容", null=True, blank=True)
    audio = models.FileField(upload_to=chat_image_path, verbose_name="相关音频", null=True, blank=True)
    related_id = models.IntegerField(default=0, verbose_name="相关绑定id")      # 对于活动消息而言这里存储的是对应活动的id

    deleted = models.BooleanField(default=False, verbose_name="是否已经被删除")
    read = models.BooleanField(default=False, verbose_name="是否已读")

    def dict_description(self):
        result =  dict(
            chatID=self.id,
            sender=self.sender.profile.simple_dict_description(),
            chat_type=self.chat_type,
            target_id=self.target_id,
            message_type=self.message_type,
            image=self.image.url if self.image else None,
            text_content=self.text_content,
            audio=self.audio.url if self.audio else None,
            related_id=self.related_id,
            created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S %Z'),
            read=self.read
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
        target_id = instance.target_user.id
    else:
        target_id = instance.target_club.id
    instance.distinct_identifier = "{0}_{1}".format(target_id, instance.chat_type)

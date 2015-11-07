# coding=utf-8
from django.db import models
from django.conf import settings

from custom.utils import path_creator
# Create your models here.


@path_creator
def chat_image_path():
    return 'chat_image'


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    club = models.ForeignKey('Club.Club', u'发生的群聊')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'发布时间')

    content = models.CharField(max_length=255, verbose_name=u'正文内容')
    image = models.ImageField(upload_to=chat_image_path, verbose_name=u'聊天图片', help_text=u'一次一张')
    inform_of = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_need_to_read', verbose_name=u'@')

    class Meta:
        verbose_name = u'聊天记录'
        verbose_name_plural = u'聊天记录'
        ordering = ['-created_at']

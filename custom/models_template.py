# coding=utf-8
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import smart_str
from django.core.exceptions import ValidationError

from .utils import path_creator


def comment_image_path(instance, filename, *args, **kwargs):
    current = timezone.now()
    ext = filename.split('.')[-1]
    random_file_name = str(uuid.uuid4()).replace('-', '')
    new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".\
        format('comment_images', current.year, current.month, current.day, random_file_name, ext)
    return new_file_name


class BaseCommentManager(models.Manager):

    def create(self, *args, **kwargs):
        image = kwargs.get('image', None)
        content = kwargs.get('content', None)
        if image is None and (content is None or content == ''):
            raise ValidationError(code='3003', message=u'评论应当至少包含图片和文字中的一个')
        return super(BaseCommentManager, self).create(*args, **kwargs)

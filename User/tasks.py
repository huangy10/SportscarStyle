# coding=utf-8
from PIL import Image
import StringIO
import os

from django.core.files.uploadedfile import InMemoryUploadedFile

from SportscarStyle.celery import app
from custom.utils import get_logger
from models import User, UserRelation
from Status.models import Status
from Activity.models import Activity


logger = get_logger(__name__)


@app.task()
def resize_image(instance, field_name, target_size):
    width, height = [float(x) for x in target_size]
    with Image.open(getattr(instance, field_name)) as im:
        w, h = im.size
        if w == width and h == height:
            return
        if w / width * height < h:
            tmp_h = int(width / w * h)
            new_im = im.resize((int(width), tmp_h), resample=Image.LANCZOS)
            new_im = new_im.crop((0, tmp_h / 2 - int(height) / 2, int(width), tmp_h / 2 + int(height) / 2))
        else:
            tmp_w = int(height / h * w)
            new_im = im.resize((tmp_w, int(height)), resample=Image.LANCZOS)
            new_im = new_im.crop((tmp_w / 2 - int(width) / 2, 0, tmp_w / 2 + int(width) / 2, int(height)))
        old_path = getattr(instance, field_name).path

        zipped_io = StringIO.StringIO()
        new_im.save(zipped_io, format='JPEG')
        setattr(instance, field_name,
                InMemoryUploadedFile(file=zipped_io,
                                     field_name=None,
                                     name='foo.jpg',
                                     content_type='image/jpeg',
                                     size=zipped_io.len,
                                     charset=None)
                )

        if callable(getattr(instance, "save")):
            instance.save()

        os.remove(old_path)


@app.task()
def user_value_change(user):
    from Club.models import Club
    old_value = user.value
    user.recalculate_value(commit=True)
    if user.value != old_value:
        for club in Club.objects.filter(members=user, identified=True):
            club.recalculate_value(commit=True)
    logger.info("user value change %s" % user.username)


@app.task()
def sync_user_cache_data(user):
    """
    同步校验用户中缓存数据的正确性,主要是包括粉丝数,关注数,动态数量等
    :param user:
    :return:
    """
    status_num = Status.objects.filter(user=user, deleted=False).count()
    fans_num = UserRelation.objects.filter(target_user=user).count()
    follow_num = UserRelation.objects.filter(source_user=user).count()
    act_num = Activity.objects.filter(user=user).count()

    if status_num != user.status_num or\
            fans_num != user.fans_num or\
            follow_num != user.fans_num or\
            act_num != user.act_num:

        user.status_num = status_num
        user.fans = fans_num
        user.follows_num = follow_num
        user.act_num = act_num
        user.save()

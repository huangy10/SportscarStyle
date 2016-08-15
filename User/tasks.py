from PIL import Image
import StringIO
import os

from django.core.files.uploadedfile import InMemoryUploadedFile

from SportscarStyle.celery import app
from Club.models import Club


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
    old_value = user.value
    user.recalculate_value(commit=True)
    if user.value != old_value:
        for club in Club.objects.filter(members=user, identified=True):
            club.recalculate_value(commit=True)

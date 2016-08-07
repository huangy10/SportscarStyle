from PIL import Image

from django.core.files import File

from SportscarStyle.celery import app


@app.task()
def resize_image(instance, field_name, target_size):
    width, height = [float(x) for x in target_size]
    with Image.open(getattr(instance, field_name)) as im:
        w, h = im.size
        if w / width * height < h:
            tmp_h = int(width / w * h)
            new_im = im.resize((int(width), tmp_h), resample=Image.LANCZOS)
            new_im = new_im.crop((0, tmp_h / 2 - int(height) / 2, int(width), tmp_h / 2 + int(height) / 2))
        else:
            tmp_w = int(height / h * w)
            new_im = im.resize((tmp_w, int(height)), resample=Image.LANCZOS)
            new_im = new_im.crop((tmp_w / 2 - int(width) / 2, 0, tmp_w / 2 + int(width) / 2, int(height)))

        setattr(instance, field_name, File(new_im))

        if callable(getattr(instance, "save")):
            instance.save()

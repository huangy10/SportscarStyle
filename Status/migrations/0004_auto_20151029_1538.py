# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.models_template


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0003_auto_20151028_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuscomment',
            name='image',
            field=models.ImageField(upload_to=custom.models_template.comment_image_path, verbose_name='\u8bc4\u8bba\u56fe\u7247'),
        ),
    ]

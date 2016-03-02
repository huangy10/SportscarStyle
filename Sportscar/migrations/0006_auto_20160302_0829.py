# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0005_sportscar_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportcaridentificationrequestrecord',
            name='images',
        ),
        migrations.AddField(
            model_name='sportcaridentificationrequestrecord',
            name='drive_license',
            field=models.ImageField(default=None, upload_to=Sportscar.models.car_auth_image, verbose_name='\u9a7e\u7167'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sportcaridentificationrequestrecord',
            name='photo',
            field=models.ImageField(default=None, upload_to=Sportscar.models.car_auth_image, verbose_name='\u5408\u5f71'),
            preserve_default=False,
        ),
    ]

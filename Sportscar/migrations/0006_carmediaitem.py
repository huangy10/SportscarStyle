# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0005_auto_20160723_0103'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarMediaItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.FileField(upload_to=Sportscar.models.car_image, verbose_name='\u5173\u8054\u6587\u4ef6')),
                ('item_type', models.CharField(max_length=10, choices=[(b'image', '\u56fe\u7247'), (b'video', '\u89c6\u9891'), (b'audio', '\u97f3\u9891')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(related_name='medias', verbose_name='\u76f8\u5173\u8dd1\u8f66', to='Sportscar.Sportscar')),
            ],
        ),
    ]

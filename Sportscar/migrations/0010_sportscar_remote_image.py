# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0009_auto_20160323_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='remote_image',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u8fdc\u7a0b\u8d44\u6e90\u94fe\u63a5'),
        ),
    ]

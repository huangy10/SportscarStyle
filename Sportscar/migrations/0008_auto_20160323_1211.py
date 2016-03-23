# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0007_auto_20160323_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='remote_id',
            field=models.IntegerField(default=0, verbose_name='\u6c7d\u8f66\u4e4b\u5bb6\u5b9a\u4e49\u7684id'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='remote_id',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]

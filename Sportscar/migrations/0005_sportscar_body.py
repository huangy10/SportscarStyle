# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0004_sportcaridentificationrequestrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='body',
            field=models.CharField(default='', max_length=255, verbose_name='\u8f66\u8eab\u7ed3\u6784'),
            preserve_default=False,
        ),
    ]

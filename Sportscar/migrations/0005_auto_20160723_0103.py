# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0004_auto_20160710_0504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sportcaridentificationrequestrecord',
            options={'verbose_name': '\u8dd1\u8f66\u8ba4\u8bc1\u8bf7\u6c42', 'verbose_name_plural': '\u8dd1\u8f66\u8ba4\u8bc1\u8bf7\u6c42'},
        ),
        migrations.AddField(
            model_name='sportcaridentificationrequestrecord',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u5904\u7406'),
        ),
    ]

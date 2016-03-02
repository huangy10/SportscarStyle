# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0005_auto_20160229_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='only_host_can_invite',
            field=models.BooleanField(default=False, verbose_name='\u53ea\u6709\u7fa4\u4e3b\u80fd\u591f\u9080\u8bf7'),
        ),
        migrations.AddField(
            model_name='club',
            name='show_members_to_public',
            field=models.BooleanField(default=False, verbose_name='\u5bf9\u5916\u516c\u5e03\u6210\u5458\u4fe1\u606f'),
        ),
    ]

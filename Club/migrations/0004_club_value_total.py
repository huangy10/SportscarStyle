# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0003_auto_20160509_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='value_total',
            field=models.IntegerField(default=0, verbose_name='\u4ff1\u4e50\u90e8\u4e2d\u6240\u6709\u6210\u5458\u7684\u6240\u6709\u8ba4\u8bc1\u8f66\u8f86\u7684\u5b98\u65b9\u53c2\u8003\u4ef7\u683c\u603b\u548c'),
        ),
    ]

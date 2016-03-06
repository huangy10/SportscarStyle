# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0006_auto_20160302_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='city',
            field=models.CharField(default='', max_length=30, verbose_name='\u4ff1\u4e50\u90e8\u6240\u5728\u7684\u57ce\u5e02'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='club',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='\u4ff1\u4e50\u90e8\u662f\u5426\u88ab\u5220\u9664'),
        ),
        migrations.AddField(
            model_name='club',
            name='value_average',
            field=models.IntegerField(default=0, verbose_name='\u5747\u4ef7'),
        ),
        migrations.AddField(
            model_name='club',
            name='value_total',
            field=models.IntegerField(default=0, verbose_name='\u4ff1\u4e50\u90e8\u4e2d\u6240\u6709\u6210\u5458\u7684\u6240\u6709\u8ba4\u8bc1\u8f66\u8f86\u7684\u5b98\u65b9\u53c2\u8003\u4ef7\u683c\u603b\u548c'),
        ),
    ]

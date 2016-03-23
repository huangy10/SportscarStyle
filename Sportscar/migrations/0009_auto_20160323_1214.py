# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0008_auto_20160323_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportscar',
            name='displacement',
        ),
        migrations.RemoveField(
            model_name='sportscar',
            name='release_date',
        ),
        migrations.RemoveField(
            model_name='sportscar',
            name='seats',
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='body',
            field=models.CharField(default=b'-', max_length=255, verbose_name='\u8f66\u8eab\u7ed3\u6784'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='engine',
            field=models.CharField(default=b'-', max_length=100, verbose_name='\u53d1\u52a8\u673a'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='fuel_consumption',
            field=models.CharField(default=b'-', help_text='\u5347\u6bcf\u767e\u516c\u91cc', max_length=100, verbose_name='\u6cb9\u8017'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='max_speed',
            field=models.CharField(default=b'-', max_length=20, verbose_name='\u6700\u9ad8\u8f66\u901f'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='price',
            field=models.CharField(default=b'-', max_length=18, verbose_name='\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='transmission',
            field=models.CharField(default=b'-', max_length=100, verbose_name='\u53d8\u901f\u5668'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='zeroTo60',
            field=models.CharField(default=b'-', max_length=7, verbose_name='\u767e\u516c\u91cc\u52a0\u901f'),
        ),
    ]

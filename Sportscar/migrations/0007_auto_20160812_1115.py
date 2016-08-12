# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0006_carmediaitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='subname',
            field=models.CharField(max_length=128, verbose_name='\u5b50\u578b\u53f7\u540d\u79f0', blank=True),
        ),
        migrations.AlterField(
            model_name='carmediaitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u6dfb\u52a0\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='name',
            field=models.CharField(max_length=128, verbose_name='\u540d\u79f0(\u4e2d\u6587)'),
        ),
        migrations.AlterUniqueTogether(
            name='sportscar',
            unique_together=set([('name', 'subname')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0006_auto_20160815_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubbillboard',
            name='filter_type',
            field=models.CharField(db_index=True, max_length=20, verbose_name='\u6392\u5e8f\u7684\u7c7b\u578b', choices=[(b'total', b'\xe6\x80\xbb\xe4\xbb\xb7\xe6\x9c\x80\xe9\xab\x98'), (b'average', b'\xe5\x9d\x87\xe4\xbb\xb7\xe6\x9c\x80\xe9\xab\x98'), (b'members', b'\xe6\x88\x90\xe5\x91\x98\xe6\x95\xb0\xe9\x87\x8f'), (b'females', b'\xe7\xbe\x8e\xe5\xa5\xb3\xe6\x9c\x80\xe5\xa4\x9a')]),
        ),
        migrations.AlterField(
            model_name='clubbillboard',
            name='order',
            field=models.IntegerField(verbose_name='\u6392\u540d', db_index=True),
        ),
        migrations.AlterField(
            model_name='clubbillboard',
            name='scope',
            field=models.CharField(help_text='\u901a\u5e38\u662f\u57ce\u5e02\u7684\u540d\u79f0', max_length=50, verbose_name='\u6392\u5e8f\u8303\u56f4', db_index=True),
        ),
        migrations.AlterField(
            model_name='clubbillboard',
            name='version',
            field=models.IntegerField(verbose_name='\u7b2c*\u671f', db_index=True),
        ),
    ]

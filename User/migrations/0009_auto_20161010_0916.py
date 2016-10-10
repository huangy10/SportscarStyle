# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_auto_20160812_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticationcode',
            name='is_active',
            field=custom.fields.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='corporationauthenticationrequest',
            name='approved',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u6279\u51c6'),
        ),
        migrations.AlterField(
            model_name='corporationauthenticationrequest',
            name='revoked',
            field=custom.fields.BooleanField(default=False, verbose_name='\u7533\u8bf7\u662f\u5426\u5df2\u7ecf\u9a73\u56de'),
        ),
        migrations.AlterField(
            model_name='user',
            name='corporation_identified',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u662f\u7ecf\u8fc7\u8ba4\u8bc1\u7684\u4f01\u4e1a\u7528\u6237'),
        ),
        migrations.AlterField(
            model_name='user',
            name='register_finished',
            field=custom.fields.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userrelation',
            name='is_friend',
            field=custom.fields.BooleanField(default=False),
        ),
    ]

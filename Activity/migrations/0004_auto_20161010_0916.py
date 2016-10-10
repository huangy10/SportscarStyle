# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0003_activity_authed_user_only'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='authed_user_only',
            field=custom.fields.BooleanField(default=False, verbose_name='\u53ea\u9650\u8ba4\u8bc1\u7528\u6237\u53c2\u52a0'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='closed',
            field=custom.fields.BooleanField(default=False, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe6\x8a\xa5\xe5\x90\x8d\xe6\x98\xaf\xe5\x90\xa6\xe5\x85\xb3\xe9\x97\xad'),
        ),
        migrations.AlterField(
            model_name='activityinvitation',
            name='agree',
            field=custom.fields.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityinvitation',
            name='responsed',
            field=custom.fields.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activityjoin',
            name='approved',
            field=custom.fields.BooleanField(default=True),
        ),
    ]

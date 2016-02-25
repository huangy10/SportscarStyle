# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Location', '0003_auto_20160225_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertracking',
            name='user',
            field=models.OneToOneField(related_name='location', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
    ]

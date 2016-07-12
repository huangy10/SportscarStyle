# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import User.models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_auto_20160525_0649'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', User.models.MyUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='blacklist',
            field=models.ManyToManyField(related_name='blacklist_by', to=settings.AUTH_USER_MODEL),
        ),
    ]

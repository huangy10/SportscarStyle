# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertracking',
            name='user',
            field=models.OneToOneField(related_name='location', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
    ]

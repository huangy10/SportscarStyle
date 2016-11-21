# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Status', '0004_auto_20161010_0916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statuslikethrough',
            options={'ordering': ('like_at',)},
        ),
        migrations.AddField(
            model_name='status',
            name='recent_like_user',
            field=models.ForeignKey(related_name='+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

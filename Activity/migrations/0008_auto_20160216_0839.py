# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0007_activity_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLikeThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_acts', verbose_name='\u559c\u6b22\u8fd9\u4e2a\u6d3b\u52a8\u7684\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activitylikethrough',
            name='activity',
            field=models.ForeignKey(verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='activitylikethrough',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
    ]

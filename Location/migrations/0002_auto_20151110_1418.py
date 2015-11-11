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
        migrations.CreateModel(
            name='UserTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.RemoveField(
            model_name='location',
            name='update_time',
        ),
        migrations.RemoveField(
            model_name='location',
            name='user',
        ),
        migrations.AddField(
            model_name='usertracking',
            name='location',
            field=models.ForeignKey(verbose_name=b'\xe4\xbd\x8d\xe7\xbd\xae', to='Location.Location'),
        ),
        migrations.AddField(
            model_name='usertracking',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
    ]

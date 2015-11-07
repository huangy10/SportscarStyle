# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Sportscar', '0003_auto_20151005_0053'),
        ('Profile', '0005_userprofile_avatar_club'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('source_user', models.OneToOneField(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('target_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u5173\u7cfb',
                'verbose_name_plural': '\u7528\u6237\u5173\u7cfb',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar_car',
            field=models.ForeignKey(verbose_name='\u5934\u50cf\u8fb9\u7684\u8dd1\u8f66', blank=True, to='Sportscar.Sportscar', null=True),
        ),
    ]

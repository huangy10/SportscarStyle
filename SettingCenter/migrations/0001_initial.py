# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_accept', models.BooleanField(default=True, verbose_name='\u63a5\u53d7\u901a\u77e5')),
                ('notification_sound', models.BooleanField(default=True, verbose_name='\u58f0\u97f3')),
                ('notification_shake', models.BooleanField(default=True, verbose_name='\u9707\u52a8')),
                ('location_visible_to', models.CharField(max_length=10, choices=[(b'all', b'\xe6\x89\x80\xe6\x9c\x89\xe4\xba\xba'), (b'female_only', b'\xe4\xbb\x85\xe5\xa5\xb3\xe6\x80\xa7'), (b'male_only', b'\xe4\xbb\x85\xe7\x94\xb7\xe6\x80\xa7'), (b'none', b'\xe4\xb8\x8d\xe5\x8f\xaf\xe8\xa7\x81'), (b'only_idol', b'\xe4\xbb\x85\xe6\x88\x91\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84\xe4\xba\xba'), (b'only_fried', b'\xe4\xba\x92\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb3\xa8')])),
                ('blacklist', models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='setting_center', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=255, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('setting_center', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

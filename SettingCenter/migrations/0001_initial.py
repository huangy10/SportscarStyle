# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SettingCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notification_accept', models.BooleanField(default=True, verbose_name='\u63a5\u53d7\u901a\u77e5')),
                ('notification_sound', models.BooleanField(default=True, verbose_name='\u58f0\u97f3')),
                ('notification_shake', models.BooleanField(default=True, verbose_name='\u9707\u52a8')),
                ('location_visible_to', models.CharField(default=b'all', max_length=10, choices=[(b'all', b'\xe6\x89\x80\xe6\x9c\x89\xe4\xba\xba'), (b'female_only', b'\xe4\xbb\x85\xe5\xa5\xb3\xe6\x80\xa7'), (b'male_only', b'\xe4\xbb\x85\xe7\x94\xb7\xe6\x80\xa7'), (b'none', b'\xe4\xb8\x8d\xe5\x8f\xaf\xe8\xa7\x81'), (b'only_idol', b'\xe4\xbb\x85\xe6\x88\x91\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84\xe4\xba\xba'), (b'only_fried', b'\xe4\xba\x92\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb3\xa8')])),
                ('accept_invitation', models.CharField(default=b'all', max_length=20, choices=[(b'all', b'\xe6\x89\x80\xe6\x9c\x89\xe4\xba\xba'), (b'friend', b'\xe4\xba\x92\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb3\xa8'), (b'follow', b'\xe6\x88\x91\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84'), (b'fans', b'\xe6\x88\x91\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84'), (b'auth_first', b'\xe9\x9c\x80\xe9\x80\x9a\xe8\xbf\x87\xe9\xaa\x8c\xe8\xaf\x81'), (b'never', b'\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8')])),
                ('show_on_map', models.BooleanField(default=True, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb1\x95\xe7\x8e\xb0\xe5\x9c\xa8\xe5\x9c\xb0\xe5\x9b\xbe\xe4\xb8\x8a')),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=255, verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
    ]

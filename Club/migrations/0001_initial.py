# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import Club.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u4ff1\u4e50\u90e8\u540d\u79f0')),
                ('logo', models.ImageField(upload_to=Club.models.club_logo, verbose_name='\u4ff1\u4e50\u90e8\u6807\u8bc6')),
                ('description', models.TextField(verbose_name='\u4ff1\u4e50\u90e8\u7b80\u4ecb')),
                ('identified', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xae\xa4\xe8\xaf\x81')),
                ('identified_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('city', models.CharField(max_length=30, verbose_name='\u4ff1\u4e50\u90e8\u6240\u5728\u7684\u57ce\u5e02')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('value_total', models.IntegerField(default=0, verbose_name='\u4ff1\u4e50\u90e8\u4e2d\u6240\u6709\u6210\u5458\u7684\u6240\u6709\u8ba4\u8bc1\u8f66\u8f86\u7684\u5b98\u65b9\u53c2\u8003\u4ef7\u683c\u603b\u548c')),
                ('value_average', models.IntegerField(default=0, verbose_name='\u5747\u4ef7')),
                ('only_host_can_invite', models.BooleanField(default=False, verbose_name='\u53ea\u6709\u7fa4\u4e3b\u80fd\u591f\u9080\u8bf7')),
                ('show_members_to_public', models.BooleanField(default=False, verbose_name='\u5bf9\u5916\u516c\u5e03\u6210\u5458\u4fe1\u606f')),
                ('deleted', models.BooleanField(default=False, verbose_name='\u4ff1\u4e50\u90e8\u662f\u5426\u88ab\u5220\u9664')),
            ],
            options={
                'verbose_name': '\u4ff1\u4e50\u90e8',
                'verbose_name_plural': '\u4ff1\u4e50\u90e8',
            },
        ),
        migrations.CreateModel(
            name='ClubAuthRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approve', models.BooleanField(default=False)),
                ('checked', models.BooleanField(default=False)),
                ('city', models.CharField(default=b'', max_length=100, verbose_name=b'\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8\xe6\x89\x80\xe5\xa4\x84\xe7\x9a\x84\xe5\x9f\x8e\xe5\xb8\x82')),
                ('description', models.CharField(default=b'', max_length=100, verbose_name=b'\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8\xe7\xae\x80\xe4\xbb\x8b')),
            ],
        ),
        migrations.CreateModel(
            name='ClubJoining',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick_name', models.CharField(max_length=100, verbose_name='\u672c\u7fa4\u6635\u79f0')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='\u52a0\u5165\u65e5\u671f')),
                ('show_nick_name', models.BooleanField(default=True, verbose_name='\u663e\u793a\u672c\u7fa4\u6210\u5458\u6635\u79f0')),
                ('no_disturbing', models.BooleanField(default=False, verbose_name='\u6d88\u606f\u514d\u6253\u6270')),
                ('always_on_top', models.BooleanField(default=False, verbose_name='\u7f6e\u9876\u804a\u5929')),
                ('always_on_to_date', models.DateTimeField(null=True, verbose_name='\u7f6e\u9876\u7684\u65e5\u671f', blank=True)),
                ('unread_chats', models.IntegerField(default=0, verbose_name='\u672a\u8bfb\u6d88\u606f\u6570\u91cf')),
                ('club', models.ForeignKey(verbose_name='\u4ff1\u4e50\u90e8', to='Club.Club')),
            ],
        ),
    ]

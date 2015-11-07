# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Club.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u4ff1\u4e50\u90e8\u540d\u79f0')),
                ('logo', models.ImageField(upload_to=Club.models.club_logo, verbose_name='\u4ff1\u4e50\u90e8\u6807\u8bc6')),
                ('description', models.TextField(verbose_name='\u4ff1\u4e50\u90e8\u7b80\u4ecb')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
                ('host', models.ForeignKey(related_name='club_started', verbose_name='\u53d1\u8d77\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4ff1\u4e50\u90e8',
                'verbose_name_plural': '\u4ff1\u4e50\u90e8',
            },
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
                ('club', models.ForeignKey(verbose_name='\u4ff1\u4e50\u90e8', to='Club.Club')),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u6210\u5458', through='Club.ClubJoining'),
        ),
    ]

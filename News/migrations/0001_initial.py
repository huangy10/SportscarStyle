# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.models_template
import News.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cover', models.ImageField(upload_to=News.models.cover_path, null=True, verbose_name='\u5c01\u9762')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898')),
                ('content', models.TextField(verbose_name='\u6b63\u6587')),
                ('video', models.FileField(upload_to=News.models.video_path, null=True, verbose_name='\u89c6\u9891')),
                ('shared_times', models.PositiveIntegerField(default=0, verbose_name='\u88ab\u5206\u4eab\u6b21\u6570')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65e5\u671f')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': '\u8d44\u8baf',
                'verbose_name_plural': '\u8d44\u8baf',
            },
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('image', models.ImageField(upload_to=custom.models_template.comment_image_path, verbose_name='\u8bc4\u8bba\u56fe\u7247', blank=True)),
                ('content', models.CharField(max_length=255, null=True, verbose_name='\u8bc4\u8bba\u6b63\u6587', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u54a8\u8be2\u8bc4\u8bba',
                'verbose_name_plural': '\u54a8\u8be2\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='NewsLikeThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like_at', models.DateTimeField(auto_now_add=True)),
                ('news', models.ForeignKey(to='News.News')),
            ],
            options={
                'ordering': ('-like_at',),
            },
        ),
    ]

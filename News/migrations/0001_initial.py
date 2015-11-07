# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import News.models
import custom.models_template
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('inform_of', models.ManyToManyField(related_name='need_to_see_comments', verbose_name='@\u67d0\u4eba', to=settings.AUTH_USER_MODEL)),
                ('news', models.ForeignKey(related_name='comments', to='News.News')),
                ('response_to', models.ForeignKey(related_name='responses', to='News.NewsComment', null=True)),
                ('user', models.ForeignKey(verbose_name='\u53d1\u5e03\u7528\u6237', to=settings.AUTH_USER_MODEL)),
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
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_news', verbose_name='\u70b9\u8d5e', through='News.NewsLikeThrough', to=settings.AUTH_USER_MODEL),
        ),
    ]

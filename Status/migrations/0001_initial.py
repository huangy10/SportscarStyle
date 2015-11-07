# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.models_template
import Status.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0003_auto_20151005_0053'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=Status.models.status_image_path, verbose_name='\u72b6\u6001\u56fe')),
                ('content', models.CharField(max_length=255, verbose_name='\u6b63\u6587')),
                ('car', models.ForeignKey(verbose_name='\u7b7e\u540d\u8dd1\u8f66', to='Sportscar.Sportscar')),
                ('inform_of', models.ManyToManyField(related_name='status_need_to_see', verbose_name='\u63d0\u9192\u8c01\u770b', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u72b6\u6001',
                'verbose_name_plural': '\u72b6\u6001',
            },
        ),
        migrations.CreateModel(
            name='StatusComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('image', models.ImageField(upload_to=custom.models_template.comment_image_path, verbose_name='\u8bc4\u8bba\u56fe\u7247', blank=True)),
                ('content', models.CharField(max_length=255, null=True, verbose_name='\u8bc4\u8bba\u6b63\u6587', blank=True)),
                ('inform_of', models.ManyToManyField(related_name='status_comments_need_to_see', verbose_name='@\u67d0\u4eba', to=settings.AUTH_USER_MODEL)),
                ('response_to', models.ForeignKey(related_name='responses', to='Status.StatusComment', null=True)),
                ('status', models.ForeignKey(related_name='comments', to='Status.Status')),
                ('user', models.ForeignKey(related_name='+', verbose_name='\u53d1\u5e03\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u72b6\u6001\u8bc4\u8bba',
                'verbose_name_plural': '\u72b6\u6001\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='StatusLikeThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.ForeignKey(to='Status.Status')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='status',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_status', verbose_name='\u70b9\u8d5e', through='Status.StatusLikeThrough', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='status',
            name='location',
            field=models.ForeignKey(verbose_name='\u53d1\u5e03\u5730\u70b9', to='Location.Location'),
        ),
        migrations.AddField(
            model_name='status',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Activity.models
import django.utils.timezone
import custom.models_template


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u6d3b\u52a8\u540d\u79f0')),
                ('description', models.TextField(verbose_name='\u6d3b\u52a8\u63cf\u8ff0')),
                ('max_attend', models.PositiveIntegerField(default=0, verbose_name='\u4eba\u6570\u4e0a\u9650')),
                ('start_at', models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_at', models.DateTimeField(verbose_name='\u7ed3\u675f\u65f6\u95f4')),
                ('poster', models.ImageField(upload_to=Activity.models.activity_poster, verbose_name='\u6d3b\u52a8\u6d77\u62a5')),
                ('closed', models.BooleanField(default=False, verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8\xe6\x8a\xa5\xe5\x90\x8d\xe6\x98\xaf\xe5\x90\xa6\xe5\x85\xb3\xe9\x97\xad')),
                ('closed_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x85\xb3\xe9\x97\xad\xe6\x8a\xa5\xe5\x90\x8d\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4')),
                ('like_num', models.IntegerField(default=0)),
                ('comment_num', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': '\u6d3b\u52a8',
                'verbose_name_plural': '\u6d3b\u52a8',
            },
        ),
        migrations.CreateModel(
            name='ActivityComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=custom.models_template.comment_image_path, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x9b\xbe\xe7\x89\x87')),
                ('content', models.CharField(max_length=255, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\xad\xa3\xe6\x96\x87')),
            ],
            options={
                'verbose_name': '\u6d3b\u52a8\u8bc4\u8bba',
                'verbose_name_plural': '\u6d3b\u52a8\u8bc4\u8bba\u5185\u5bb9',
            },
        ),
        migrations.CreateModel(
            name='ActivityInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('responsed', models.BooleanField(default=False)),
                ('agree', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': '\u6d3b\u52a8\u9080\u8bf7',
                'verbose_name_plural': '\u6d3b\u52a8\u9080\u8bf7',
            },
        ),
        migrations.CreateModel(
            name='ActivityJoin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ActivityLikeThrough',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(verbose_name=b'\xe6\xb4\xbb\xe5\x8a\xa8', to='Activity.Activity')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]

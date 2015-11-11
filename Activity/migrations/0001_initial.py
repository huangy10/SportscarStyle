# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.models_template
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Location', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Club', '0001_initial'),
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
                ('allowed_club', models.ForeignKey(verbose_name='\u5141\u8bb8\u52a0\u5165\u7684\u4ff1\u4e50\u90e8', blank=True, to='Club.Club')),
                ('inform_of', models.ManyToManyField(related_name='activities_need_to_see', verbose_name='\u901a\u77e5\u8c01\u770b', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(verbose_name='\u6d3b\u52a8\u5730\u70b9', to='Location.Location')),
            ],
            options={
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
                ('activity', models.ForeignKey(related_name='comments', verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb4\xbb\xe5\x8a\xa8', to='Activity.Activity')),
                ('inform_of', models.ManyToManyField(related_name='activity_comments_need_to_see', verbose_name=b'@\xe6\x9f\x90\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
                ('response_to', models.ForeignKey(related_name='responses', blank=True, to='Activity.ActivityComment', null=True)),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6d3b\u52a8\u8bc4\u8bba',
                'verbose_name_plural': '\u6d3b\u52a8\u8bc4\u8bba\u5185\u5bb9',
            },
        ),
        migrations.CreateModel(
            name='ActivityJoin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(related_name='+', to='Activity.Activity')),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

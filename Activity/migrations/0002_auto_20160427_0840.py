# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0001_initial'),
        ('Club', '0001_initial'),
        ('Location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylikethrough',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activityjoin',
            name='activity',
            field=models.ForeignKey(related_name='applications', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='activityjoin',
            name='user',
            field=models.ForeignKey(related_name='applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activityinvitation',
            name='activity',
            field=models.ForeignKey(to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='activityinvitation',
            name='inviter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activityinvitation',
            name='target',
            field=models.ForeignKey(related_name='invites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activitycomment',
            name='activity',
            field=models.ForeignKey(related_name='comments', verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb4\xbb\xe5\x8a\xa8', to='Activity.Activity'),
        ),
        migrations.AddField(
            model_name='activitycomment',
            name='inform_of',
            field=models.ManyToManyField(related_name='activity_comments_need_to_see', verbose_name=b'@\xe6\x9f\x90\xe4\xba\xba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activitycomment',
            name='response_to',
            field=models.ForeignKey(related_name='responses', blank=True, to='Activity.ActivityComment', null=True),
        ),
        migrations.AddField(
            model_name='activitycomment',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='allowed_club',
            field=models.ForeignKey(verbose_name='\u5141\u8bb8\u52a0\u5165\u7684\u4ff1\u4e50\u90e8', blank=True, to='Club.Club', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='appliers',
            field=models.ManyToManyField(related_name='applied_acts', verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe8\x80\x85', through='Activity.ActivityJoin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='inform_of',
            field=models.ManyToManyField(related_name='activities_need_to_see', verbose_name='\u901a\u77e5\u8c01\u770b', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_acts', verbose_name='\u559c\u6b22\u8fd9\u4e2a\u6d3b\u52a8\u7684\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.ForeignKey(verbose_name='\u6d3b\u52a8\u5730\u70b9', to='Location.Location'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(verbose_name='\u6d3b\u52a8\u53d1\u8d77\u8005', to=settings.AUTH_USER_MODEL),
        ),
    ]

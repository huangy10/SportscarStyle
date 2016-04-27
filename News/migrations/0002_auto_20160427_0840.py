# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('News', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslikethrough',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newscomment',
            name='inform_of',
            field=models.ManyToManyField(related_name='news_comments_need_to_see', verbose_name='@\u67d0\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newscomment',
            name='news',
            field=models.ForeignKey(related_name='comments', to='News.News'),
        ),
        migrations.AddField(
            model_name='newscomment',
            name='response_to',
            field=models.ForeignKey(related_name='responses', to='News.NewsComment', null=True),
        ),
        migrations.AddField(
            model_name='newscomment',
            name='user',
            field=models.ForeignKey(related_name='+', verbose_name='\u53d1\u5e03\u7528\u6237', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_news', verbose_name='\u70b9\u8d5e', through='News.NewsLikeThrough', to=settings.AUTH_USER_MODEL),
        ),
    ]

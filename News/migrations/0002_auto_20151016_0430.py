# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newscomment',
            name='inform_of',
            field=models.ManyToManyField(related_name='news_comments_need_to_see', verbose_name='@\u67d0\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='newscomment',
            name='user',
            field=models.ForeignKey(related_name='+', verbose_name='\u53d1\u5e03\u7528\u6237', to=settings.AUTH_USER_MODEL),
        ),
    ]

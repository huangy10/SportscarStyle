# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0002_auto_20160427_0840'),
        ('Notification', '0001_initial'),
        ('Status', '0001_initial'),
        ('Club', '0002_auto_20160427_0840'),
        ('News', '0002_auto_20160427_0840'),
        ('Sportscar', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereddevices',
            name='user',
            field=models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_act',
            field=models.ForeignKey(related_name='+', to='Activity.Activity', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_act_comment',
            field=models.ForeignKey(related_name='+', to='Activity.ActivityComment', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_act_invite',
            field=models.ForeignKey(related_name='+', to='Activity.ActivityInvitation', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_act_join',
            field=models.ForeignKey(related_name='+', to='Activity.ActivityJoin', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_club',
            field=models.ForeignKey(related_name='+', to='Club.Club', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_news',
            field=models.ForeignKey(related_name='+', to='News.News', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_news_comment',
            field=models.ForeignKey(related_name='+', to='News.NewsComment', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_own',
            field=models.ForeignKey(related_name='+', to='Sportscar.SportCarOwnership', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_status',
            field=models.ForeignKey(related_name='+', to='Status.Status', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_status_comment',
            field=models.ForeignKey(related_name='+', to='Status.StatusComment', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='related_user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='target',
            field=models.ForeignKey(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL),
        ),
    ]

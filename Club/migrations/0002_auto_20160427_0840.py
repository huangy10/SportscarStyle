# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Club', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubjoining',
            name='user',
            field=models.ForeignKey(related_name='clubs', verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clubauthrequest',
            name='club',
            field=models.ForeignKey(verbose_name=b'\xe5\xbe\x85\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8', to='Club.Club'),
        ),
        migrations.AddField(
            model_name='club',
            name='host',
            field=models.ForeignKey(related_name='club_started', verbose_name='\u53d1\u8d77\u8005', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u6210\u5458', through='Club.ClubJoining'),
        ),
        migrations.AlterUniqueTogether(
            name='clubjoining',
            unique_together=set([('user', 'club')]),
        ),
    ]

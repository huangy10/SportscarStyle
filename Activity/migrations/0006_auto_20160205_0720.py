# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0005_activity_created_at'),
    ]

    operations = [
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
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ('-created_at',), 'verbose_name': '\u6d3b\u52a8', 'verbose_name_plural': '\u6d3b\u52a8'},
        ),
        migrations.AlterModelOptions(
            name='activityjoin',
            options={'ordering': ('-created_at',)},
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
    ]

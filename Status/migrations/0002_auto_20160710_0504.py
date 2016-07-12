# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Status', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=255)),
                ('checked', models.BooleanField(default=False)),
                ('flag', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u4e3e\u62a5\u4fe1\u606f',
                'verbose_name_plural': '\u4e3e\u62a5\u4fe1\u606f',
            },
        ),
        migrations.AlterField(
            model_name='status',
            name='content',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u6b63\u6587'),
        ),
        migrations.AddField(
            model_name='statusreport',
            name='status',
            field=models.ForeignKey(to='Status.Status'),
        ),
        migrations.AddField(
            model_name='statusreport',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

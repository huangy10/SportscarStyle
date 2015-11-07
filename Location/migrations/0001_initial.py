# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='\u5f53\u524d\u4f4d\u7f6e')),
                ('description', models.CharField(max_length=255, verbose_name='\u5730\u7406\u4fe1\u606f\u63cf\u8ff0')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4f4d\u7f6e\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.ForeignKey(related_name='location', verbose_name='\u7528\u6237\u540d', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4f4d\u7f6e',
                'verbose_name_plural': '\u4f4d\u7f6e',
            },
        ),
    ]

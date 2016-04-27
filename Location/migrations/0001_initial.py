# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='\u5f53\u524d\u4f4d\u7f6e')),
                ('description', models.CharField(max_length=255, verbose_name='\u5730\u7406\u4fe1\u606f\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': '\u4f4d\u7f6e',
                'verbose_name_plural': '\u4f4d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='UserTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('location_available', models.BooleanField(default=False, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80\xe6\x95\xb0\xe6\x8d\xae\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\xaf\xe7\x94\xa8')),
                ('location', models.ForeignKey(verbose_name=b'\xe4\xbd\x8d\xe7\xbd\xae', to='Location.Location')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]

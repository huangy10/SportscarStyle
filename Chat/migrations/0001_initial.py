# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Chat.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatRecordBasic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chat_type', models.CharField(max_length=10, choices=[(b'private', b'private'), (b'group', b'group')])),
                ('distinct_identifier', models.CharField(max_length=20)),
                ('message_type', models.CharField(max_length=15, choices=[(b'text', b'text'), (b'image', b'image'), (b'audio', b'audio'), (b'activity', b'activity'), (b'share', b'share'), (b'contact', b'contact'), (b'placeholder', b'placeholder')])),
                ('image', models.ImageField(upload_to=Chat.models.chat_image_path, null=True, verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe5\x9b\xbe\xe7\x89\x87', blank=True)),
                ('text_content', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x96\x87\xe5\xad\x97\xe5\x86\x85\xe5\xae\xb9', blank=True)),
                ('audio', models.FileField(upload_to=Chat.models.chat_image_path, null=True, verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe9\x9f\xb3\xe9\xa2\x91', blank=True)),
                ('related_id', models.IntegerField(default=0, verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe7\xbb\x91\xe5\xae\x9aid')),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe8\xa2\xab\xe5\x88\xa0\xe9\x99\xa4')),
                ('read', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe8\xaf\xbb')),
            ],
            options={
                'ordering': ('distinct_identifier', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='RosterItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import Chat.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Club', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('content', models.CharField(max_length=255, verbose_name='\u6b63\u6587\u5185\u5bb9')),
                ('image', models.ImageField(help_text='\u4e00\u6b21\u4e00\u5f20', upload_to=Chat.models.chat_image_path, verbose_name='\u804a\u5929\u56fe\u7247')),
                ('club', models.ForeignKey(verbose_name='\u53d1\u751f\u7684\u7fa4\u804a', to='Club.Club')),
                ('inform_of', models.ManyToManyField(related_name='chat_need_to_read', verbose_name='@', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '\u804a\u5929\u8bb0\u5f55',
                'verbose_name_plural': '\u804a\u5929\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='ChatRecordBasic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chat_type', models.IntegerField(default=0, choices=[(0, b'private'), (1, b'group')])),
                ('target_id', models.IntegerField(default=0, verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87id')),
                ('message_type', models.IntegerField(default=0, choices=[(0, b'text'), (1, b'image'), (2, b'voice'), (3, b'activity'), (4, b'share'), (5, b'contact')])),
                ('image', models.ImageField(upload_to=Chat.models.chat_image_path, null=True, verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe5\x9b\xbe\xe7\x89\x87', blank=True)),
                ('text_content', models.CharField(max_length=255, null=True, verbose_name=b'\xe6\x96\x87\xe5\xad\x97\xe5\x86\x85\xe5\xae\xb9', blank=True)),
                ('audio', models.FileField(upload_to=Chat.models.chat_image_path, null=True, verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe9\x9f\xb3\xe9\xa2\x91', blank=True)),
                ('related_id', models.IntegerField(default=0, verbose_name=b'\xe7\x9b\xb8\xe5\x85\xb3\xe7\xbb\x91\xe5\xae\x9aid')),
                ('deleted', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe8\xa2\xab\xe5\x88\xa0\xe9\x99\xa4')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

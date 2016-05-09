# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import Chat.models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20160503_0453'),
        ('Club', '0002_auto_20160427_0840'),
        ('Chat', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chat_type', models.CharField(max_length=10, choices=[(b'user', b'user'), (b'club', b'club')])),
                ('message_type', models.CharField(max_length=15, choices=[(b'text', b'text'), (b'image', b'image'), (b'audio', b'audio'), (b'placeholder', b'placeholder')])),
                ('image', models.ImageField(null=True, upload_to=Chat.models.chat_image_path, blank=True)),
                ('text', models.CharField(max_length=255, null=True, blank=True)),
                ('audio', models.FileField(null=True, upload_to=Chat.models.chat_image_path, blank=True)),
                ('audio_wave_data', models.CharField(default=b'', max_length=255)),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(related_name='chats', to='User.User')),
                ('target_club', models.ForeignKey(related_name='chats', blank=True, to='Club.Club', null=True)),
                ('target_user', models.ForeignKey(related_name='chats_to_me', blank=True, to='User.User', null=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.RemoveField(
            model_name='chatrecordbasic',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='chatrecordbasic',
            name='target_club',
        ),
        migrations.RemoveField(
            model_name='chatrecordbasic',
            name='target_user',
        ),
        migrations.DeleteModel(
            name='RosterItem',
        ),
        migrations.AlterModelOptions(
            name='chatentity',
            options={'ordering': ('-updated_at',), 'verbose_name': '\u82b1\u540d\u518c\u9879', 'verbose_name_plural': '\u82b1\u540d\u518c\u9879'},
        ),
        migrations.AddField(
            model_name='chatentity',
            name='always_on_top',
            field=models.BooleanField(default=False, verbose_name='\u804a\u5929\u7f6e\u9876'),
        ),
        migrations.AddField(
            model_name='chatentity',
            name='club',
            field=models.ForeignKey(related_name='+', verbose_name='\u5173\u8054\u7684\u7fa4\u804a', blank=True, to='Club.ClubJoining', null=True),
        ),
        migrations.AddField(
            model_name='chatentity',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 3, 4, 56, 51, 109086, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatentity',
            name='host',
            field=models.ForeignKey(related_name='rosters', default='', verbose_name='\u6240\u6709\u8005', to='User.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatentity',
            name='no_disturbing',
            field=models.BooleanField(default=False, verbose_name='\u6d88\u606f\u514d\u6253\u6270'),
        ),
        migrations.AddField(
            model_name='chatentity',
            name='unread_num',
            field=models.IntegerField(default=0, verbose_name='\u672a\u8bfb\u6d88\u606f\u6570\u91cf'),
        ),
        migrations.AddField(
            model_name='chatentity',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 3, 4, 57, 1, 932869, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatentity',
            name='user',
            field=models.ForeignKey(related_name='+', verbose_name='\u5173\u8054\u7684\u7528\u6237', blank=True, to='User.User', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='chatentity',
            unique_together=set([('user', 'host')]),
        ),
        migrations.DeleteModel(
            name='ChatRecordBasic',
        ),
    ]

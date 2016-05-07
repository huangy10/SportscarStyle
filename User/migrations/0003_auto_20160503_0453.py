# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import User.models


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0001_initial'),
        ('User', '0002_user_register_finished'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationAuthenticationRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('license_image', models.ImageField(upload_to=User.models.auth_image, verbose_name='\u8425\u4e1a\u6267\u7167')),
                ('id_card_image', models.ImageField(upload_to=User.models.auth_image, verbose_name='\u8eab\u4efd\u8bc1\u56fe\u7247')),
                ('other_info_image', models.ImageField(upload_to=User.models.auth_image, verbose_name='\u8865\u5145\u6750\u6599')),
                ('approved', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u6279\u51c6')),
                ('revoked', models.BooleanField(default=False, verbose_name='\u7533\u8bf7\u662f\u5426\u5df2\u7ecf\u9a73\u56de')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': '\u4f01\u4e1a\u7533\u8bf7',
                'verbose_name_plural': '\u4f01\u4e1a\u7533\u8bf7',
            },
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='most_recent_status',
            field=models.ForeignKey(related_name='+', blank=True, to='Status.Status', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar_club',
            field=models.ForeignKey(related_name='+', blank=True, to='Club.ClubJoining', null=True),
        ),
        migrations.AddField(
            model_name='corporationauthenticationrequest',
            name='user',
            field=models.ForeignKey(verbose_name='\u7533\u8bf7\u4eba', to='User.User'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Profile.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Profile', '0015_auto_20160211_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporationUserApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe6\x97\xa5\xe6\x9c\x9f')),
                ('license_image', models.ImageField(upload_to=Profile.models.auth_image, verbose_name=b'\xe8\x90\xa5\xe4\xb8\x9a\xe6\x89\xa7\xe7\x85\xa7\xe5\x9b\xbe\xe7\x89\x87')),
                ('id_card_image', models.ImageField(upload_to=Profile.models.auth_image, verbose_name=b'\xe8\xba\xab\xe4\xbb\xbd\xe8\xaf\x81\xe5\x9b\xbe\xe7\x89\x87')),
                ('other_info_image', models.ImageField(upload_to=Profile.models.auth_image, verbose_name=b'\xe8\xa1\xa5\xe5\x85\x85\xe6\x9d\x90\xe6\x96\x99')),
                ('approved', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe7\xbb\x8f\xe6\x89\xb9\xe5\x87\x86')),
                ('user', models.ForeignKey(verbose_name=b'\xe7\x94\xb3\xe8\xaf\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': '\u4f01\u4e1a\u8ba4\u8bc1\u7533\u8bf7',
                'verbose_name_plural': '\u4f01\u4e1a\u8ba4\u8bc1\u7533\u8bf7',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='corporation_user',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe7\xbb\x8f\xe8\xbf\x87\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe4\xbc\x81\xe4\xb8\x9a\xe7\x94\xa8\xe6\x88\xb7'),
        ),
    ]

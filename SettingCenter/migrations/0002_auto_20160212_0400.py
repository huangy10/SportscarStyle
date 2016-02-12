# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SettingCenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingcenter',
            name='accept_invitation',
            field=models.CharField(default=b'all', max_length=20, choices=[(b'all', b'\xe6\x89\x80\xe6\x9c\x89\xe4\xba\xba'), (b'friend', b'\xe4\xba\x92\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb3\xa8'), (b'follow', b'\xe6\x88\x91\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84'), (b'fans', b'\xe6\x88\x91\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84'), (b'auth_first', b'\xe9\x9c\x80\xe9\x80\x9a\xe8\xbf\x87\xe9\xaa\x8c\xe8\xaf\x81'), (b'never', b'\xe4\xb8\x8d\xe5\x85\x81\xe8\xae\xb8')]),
        ),
    ]

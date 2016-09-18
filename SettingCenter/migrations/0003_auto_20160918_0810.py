# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SettingCenter', '0002_auto_20160427_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingcenter',
            name='location_visible_to',
            field=models.CharField(default=b'all', max_length=20, choices=[(b'all', b'\xe6\x89\x80\xe6\x9c\x89\xe4\xba\xba'), (b'female_only', b'\xe4\xbb\x85\xe5\xa5\xb3\xe6\x80\xa7'), (b'male_only', b'\xe4\xbb\x85\xe7\x94\xb7\xe6\x80\xa7'), (b'none', b'\xe4\xb8\x8d\xe5\x8f\xaf\xe8\xa7\x81'), (b'only_idol', b'\xe4\xbb\x85\xe6\x88\x91\xe5\x85\xb3\xe6\xb3\xa8\xe7\x9a\x84\xe4\xba\xba'), (b'only_fried', b'\xe4\xba\x92\xe7\x9b\xb8\xe5\x85\xb3\xe6\xb3\xa8')]),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0009_auto_20160324_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubauthrequest',
            name='city',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8\xe6\x89\x80\xe5\xa4\x84\xe7\x9a\x84\xe5\x9f\x8e\xe5\xb8\x82'),
        ),
        migrations.AlterField(
            model_name='clubauthrequest',
            name='description',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8\xe7\xae\x80\xe4\xbb\x8b'),
        ),
    ]

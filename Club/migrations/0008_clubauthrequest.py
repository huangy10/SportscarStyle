# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0007_auto_20160306_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubAuthRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approve', models.BooleanField(default=False)),
                ('club', models.ForeignKey(verbose_name=b'\xe5\xbe\x85\xe8\xae\xa4\xe8\xaf\x81\xe7\x9a\x84\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8', to='Club.Club')),
            ],
        ),
    ]

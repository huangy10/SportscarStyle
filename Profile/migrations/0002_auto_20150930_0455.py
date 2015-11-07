# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authenticationcode',
            old_name='phoneNum',
            new_name='phone_num',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Location', '0003_location_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertracking',
            name='location_available',
            field=custom.fields.BooleanField(default=False, verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80\xe6\x95\xb0\xe6\x8d\xae\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\xaf\xe7\x94\xa8'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clubjoining',
            unique_together=set([('user', 'club')]),
        ),
    ]

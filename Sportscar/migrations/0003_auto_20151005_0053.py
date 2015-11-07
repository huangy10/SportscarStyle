# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0002_auto_20151003_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sportcarownership',
            name='identified_at',
            field=models.DateTimeField(null=True, verbose_name='\u8ba4\u8bc1\u65e5\u671f', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='sportcarownership',
            unique_together=set([('user', 'car')]),
        ),
    ]

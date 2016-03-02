# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0002_auto_20160120_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u88ab\u5220\u9664'),
        ),
    ]

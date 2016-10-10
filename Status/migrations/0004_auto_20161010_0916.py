# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0003_auto_20160723_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='deleted',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u88ab\u5220\u9664'),
        ),
        migrations.AlterField(
            model_name='statusreport',
            name='checked',
            field=custom.fields.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='statusreport',
            name='flag',
            field=custom.fields.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0009_auto_20160906_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sportcaridentificationrequestrecord',
            name='approved',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u6279\u51c6'),
        ),
        migrations.AlterField(
            model_name='sportcaridentificationrequestrecord',
            name='checked',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u5904\u7406'),
        ),
        migrations.AlterField(
            model_name='sportcarownership',
            name='identified',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u8ba4\u8bc1'),
        ),
        migrations.AlterField(
            model_name='sportscar',
            name='data_fetched',
            field=custom.fields.BooleanField(default=False, verbose_name=''),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0005_auto_20160506_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='deleted',
            field=custom.fields.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chatentity',
            name='always_on_top',
            field=custom.fields.BooleanField(default=False, verbose_name='\u804a\u5929\u7f6e\u9876'),
        ),
        migrations.AlterField(
            model_name='chatentity',
            name='no_disturbing',
            field=custom.fields.BooleanField(default=False, verbose_name='\u6d88\u606f\u514d\u6253\u6270'),
        ),
    ]

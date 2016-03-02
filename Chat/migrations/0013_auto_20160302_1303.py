# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0005_auto_20160229_1234'),
        ('Chat', '0012_auto_20160302_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatrecordbasic',
            name='target_join',
        ),
        migrations.AddField(
            model_name='chatrecordbasic',
            name='target_club',
            field=models.ForeignKey(related_name='chats', verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe7\xbe\xa4\xe8\x81\x8a', blank=True, to='Club.Club', null=True),
        ),
    ]

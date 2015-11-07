# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0002_status_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuscomment',
            name='response_to',
            field=models.ForeignKey(related_name='responses', blank=True, to='Status.StatusComment', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='statuslikethrough',
            unique_together=set([('user', 'status')]),
        ),
    ]

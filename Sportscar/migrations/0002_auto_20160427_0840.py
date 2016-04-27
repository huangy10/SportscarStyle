# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Sportscar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sportscar',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Sportscar.SportCarOwnership'),
        ),
        migrations.AddField(
            model_name='sportcarownership',
            name='car',
            field=models.ForeignKey(related_name='ownership', to='Sportscar.Sportscar'),
        ),
        migrations.AddField(
            model_name='sportcarownership',
            name='user',
            field=models.ForeignKey(related_name='ownership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sportcaridentificationrequestrecord',
            name='ownership',
            field=models.ForeignKey(verbose_name='\u5f85\u8ba4\u8bc1\u8dd1\u8f66', to='Sportscar.SportCarOwnership'),
        ),
        migrations.AlterUniqueTogether(
            name='sportcarownership',
            unique_together=set([('user', 'car')]),
        ),
    ]

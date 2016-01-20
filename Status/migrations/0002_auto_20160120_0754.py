# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Status.models


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='image',
        ),
        migrations.AddField(
            model_name='status',
            name='image1',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image2',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image3',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image4',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image5',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image6',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image7',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image8',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AddField(
            model_name='status',
            name='image9',
            field=models.ImageField(upload_to=Status.models.status_image_path, null=True, verbose_name='\u72b6\u6001\u56fe', blank=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='car',
            field=models.ForeignKey(verbose_name='\u7b7e\u540d\u8dd1\u8f66', blank=True, to='Sportscar.Sportscar', null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='location',
            field=models.ForeignKey(verbose_name='\u53d1\u5e03\u5730\u70b9', blank=True, to='Location.Location', null=True),
        ),
    ]

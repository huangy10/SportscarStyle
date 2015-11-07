# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0003_auto_20151005_0053'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportCarIdentificationRequestRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4')),
                ('approved', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6279\u51c6')),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to=Sportscar.models.car_auth_image), verbose_name='\u8ba4\u8bc1\u56fe\u7247', size=3)),
                ('id_card', models.ImageField(upload_to=Sportscar.models.car_auth_image, verbose_name='\u8eab\u4efd\u8bc1')),
                ('license_num', models.CharField(max_length=30, verbose_name='\u8f66\u724c\u53f7')),
                ('ownership', models.ForeignKey(verbose_name='\u5f85\u8ba4\u8bc1\u8dd1\u8f66', to='Sportscar.SportCarOwnership')),
            ],
        ),
    ]

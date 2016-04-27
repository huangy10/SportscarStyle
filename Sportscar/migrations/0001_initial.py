# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Sportscar.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u540d\u79f0(\u4e2d\u6587)')),
                ('remote_id', models.IntegerField(default=0, unique=True)),
                ('detail_url', models.CharField(max_length=255, verbose_name='\u8be6\u60c5\u94fe\u63a5')),
                ('logo', models.ImageField(upload_to=Sportscar.models.car_logo, verbose_name='\u5382\u5546logo')),
                ('logo_remote', models.CharField(max_length=255, verbose_name='\u5382\u5546\u7684logo\u7684url')),
                ('index', models.CharField(max_length=1, verbose_name='\u97f3\u5e8f')),
            ],
            options={
                'verbose_name': '\u6c7d\u8f66\u751f\u4ea7\u5546',
                'verbose_name_plural': '\u6c7d\u8f66\u751f\u4ea7\u5546',
            },
        ),
        migrations.CreateModel(
            name='SportCarIdentificationRequestRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4')),
                ('approved', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6279\u51c6')),
                ('drive_license', models.ImageField(upload_to=Sportscar.models.car_auth_image, verbose_name='\u9a7e\u7167')),
                ('id_card', models.ImageField(upload_to=Sportscar.models.car_auth_image, verbose_name='\u8eab\u4efd\u8bc1')),
                ('photo', models.ImageField(upload_to=Sportscar.models.car_auth_image, verbose_name='\u5408\u5f71')),
                ('license_num', models.CharField(max_length=30, verbose_name='\u8f66\u724c\u53f7')),
            ],
        ),
        migrations.CreateModel(
            name='SportCarOwnership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signature', models.CharField(max_length=255, verbose_name='\u8dd1\u8f66\u7b7e\u540d')),
                ('identified', models.BooleanField(default=False, verbose_name='\u662f\u5426\u8ba4\u8bc1')),
                ('identified_at', models.DateTimeField(null=True, verbose_name='\u8ba4\u8bc1\u65e5\u671f', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u62e5\u6709\u65e5\u671f')),
            ],
            options={
                'verbose_name': '\u62e5\u8f66/\u5173\u6ce8',
                'verbose_name_plural': '\u62e5\u8f66/\u5173\u6ce8',
            },
        ),
        migrations.CreateModel(
            name='Sportscar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u540d\u79f0(\u4e2d\u6587)')),
                ('remote_id', models.IntegerField(default=0, verbose_name='\u6c7d\u8f66\u4e4b\u5bb6\u5b9a\u4e49\u7684id')),
                ('price', models.CharField(default=b'-', max_length=18, verbose_name='\u4ef7\u683c')),
                ('fuel_consumption', models.CharField(default=b'-', help_text='\u5347\u6bcf\u767e\u516c\u91cc', max_length=100, verbose_name='\u6cb9\u8017')),
                ('engine', models.CharField(default=b'-', max_length=100, verbose_name='\u53d1\u52a8\u673a')),
                ('transmission', models.CharField(default=b'-', max_length=100, verbose_name='\u53d8\u901f\u5668')),
                ('max_speed', models.CharField(default=b'-', max_length=20, verbose_name='\u6700\u9ad8\u8f66\u901f')),
                ('zeroTo60', models.CharField(default=b'-', max_length=7, verbose_name='\u767e\u516c\u91cc\u52a0\u901f')),
                ('body', models.CharField(default=b'-', max_length=255, verbose_name='\u8f66\u8eab\u7ed3\u6784')),
                ('torque', models.CharField(default='-', max_length=255)),
                ('logo', models.ImageField(upload_to=Sportscar.models.car_logo, verbose_name='\u8f66\u6807')),
                ('image', models.ImageField(upload_to=Sportscar.models.car_image, verbose_name='\u8dd1\u8f66\u7167\u7247')),
                ('thumbnail', models.ImageField(upload_to=Sportscar.models.car_thumbnail, verbose_name='\u7f29\u7565\u56fe')),
                ('remote_image', models.CharField(default=b'', max_length=255, verbose_name='\u8fdc\u7a0b\u8d44\u6e90\u94fe\u63a5')),
                ('remote_thumbnail', models.CharField(default=b'', max_length=255, verbose_name='\u8fdc\u7a0b\u7f29\u7565\u56fe')),
                ('data_fetched', models.BooleanField(default=False, verbose_name='')),
                ('manufacturer', models.ForeignKey(verbose_name='\u5236\u9020\u5546', to='Sportscar.Manufacturer')),
            ],
            options={
                'verbose_name': '\u8dd1\u8f66',
                'verbose_name_plural': '\u8dd1\u8f66',
            },
        ),
    ]

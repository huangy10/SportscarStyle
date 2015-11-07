# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u540d\u79f0(\u4e2d\u6587)')),
                ('name_english', models.CharField(unique=True, max_length=128, verbose_name='\u540d\u79f0(\u82f1\u6587)')),
            ],
            options={
                'verbose_name': '\u6c7d\u8f66\u751f\u4ea7\u5546',
                'verbose_name_plural': '\u6c7d\u8f66\u751f\u4ea7\u5546',
            },
        ),
        migrations.CreateModel(
            name='SportCarOwnership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signature', models.CharField(max_length=255, verbose_name='\u8dd1\u8f66\u7b7e\u540d')),
                ('identified', models.BooleanField(default=False, verbose_name='\u662f\u5426\u8ba4\u8bc1')),
                ('identified_at', models.DateTimeField(verbose_name='\u8ba4\u8bc1\u65e5\u671f', blank=True)),
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
                ('name_english', models.CharField(unique=True, max_length=128, verbose_name='\u540d\u79f0(\u82f1\u6587)')),
                ('price', models.CharField(max_length=18, verbose_name='\u4ef7\u683c')),
                ('seats', models.PositiveIntegerField(default=0, verbose_name='\u5ea7\u4f4d\u6570')),
                ('fuel_consumption', models.FloatField(default=0, help_text='\u5347\u6bcf\u767e\u516c\u91cc', verbose_name='\u6cb9\u8017')),
                ('displacement', models.FloatField(default=0, help_text='\u5347', verbose_name='\u6392\u91cf')),
                ('release_date', models.DateField(verbose_name='\u53d1\u5e03\u65e5\u671f')),
                ('logo', models.ImageField(upload_to=b'', verbose_name='\u8f66\u6807')),
                ('manufacturer', models.ForeignKey(verbose_name='\u5236\u9020\u5546', to='Sportscar.Manufacturer')),
                ('owners', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Sportscar.SportCarOwnership')),
            ],
            options={
                'verbose_name': '\u8dd1\u8f66',
                'verbose_name_plural': '\u8dd1\u8f66',
            },
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
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import User.models


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0001_initial'),
        ('Club', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_num', models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('code', models.CharField(max_length=6, verbose_name='\u9a8c\u8bc1\u7801')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_friend', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=20)),
                ('nick_name', models.CharField(max_length=100)),
                ('avatar', models.ImageField(upload_to=User.models.profile_avatar)),
                ('gender', models.CharField(max_length=1, verbose_name='\u6027\u522b', choices=[(b'm', '\u7537'), (b'f', '\u5973')])),
                ('birth_date', models.DateField(verbose_name='\u51fa\u751f\u65e5\u671f')),
                ('star_sign', models.CharField(default=b'Aries', max_length=25, verbose_name='\u661f\u5ea7', choices=[(b'Aries', '\u767d\u7f8a\u5ea7'), (b'Taurus', '\u91d1\u725b\u5ea7'), (b'Gemini', '\u53cc\u5b50\u5ea7'), (b'Cancer', '\u5de8\u87f9\u5ea7'), (b'Leo', '\u72ee\u5b50\u5ea7'), (b'Virgo', '\u5904\u5973\u5ea7'), (b'Libra', '\u5929\u79e4\u5ea7'), (b'Scorpio', '\u5929\u874e\u5ea7'), (b'Sagittarius', '\u5c04\u624b\u5ea7'), (b'Capricorn', '\u6469\u7faf\u5ea7'), (b'Aquarius', '\u6c34\u74f6\u5ea7'), (b'Pisces', '\u53cc\u9c7c\u5ea7')])),
                ('district', models.CharField(default=b'', max_length=255, verbose_name='\u5730\u533a')),
                ('signature', models.CharField(default=b'', max_length=255, verbose_name='\u7b7e\u540d')),
                ('job', models.CharField(default=b'', max_length=64, verbose_name=b'\xe8\xa1\x8c\xe4\xb8\x9a')),
                ('corporation_identified', models.BooleanField(default=False, verbose_name='\u662f\u5426\u662f\u7ecf\u8fc7\u8ba4\u8bc1\u7684\u4f01\u4e1a\u7528\u6237')),
                ('fans_num', models.IntegerField(default=0, verbose_name='\u7c89\u4e1d\u6570\u91cf')),
                ('follows_num', models.IntegerField(default=0, verbose_name='\u5173\u6ce8\u6570\u91cf')),
                ('status_num', models.IntegerField(default=0, verbose_name='\u52a8\u6001\u6570\u91cf')),
                ('act_num', models.IntegerField(default=0, verbose_name='\u6d3b\u52a8\u6570\u91cf')),
                ('avatar_car', models.ForeignKey(related_name='+', blank=True, to='Sportscar.SportCarOwnership', null=True)),
                ('avatar_club', models.ForeignKey(related_name='+', blank=True, to='Club.Club', null=True)),
                ('fans', models.ManyToManyField(related_name='follows', through='User.UserRelation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='userrelation',
            name='source_user',
            field=models.ForeignKey(related_name='follows_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userrelation',
            name='target_user',
            field=models.ForeignKey(related_name='fans_relation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userrelation',
            unique_together=set([('source_user', 'target_user')]),
        ),
    ]

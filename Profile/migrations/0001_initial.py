# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Profile.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phoneNum', models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('code', models.CharField(max_length=6, verbose_name='\u9a8c\u8bc1\u7801')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProfileTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_type', models.CharField(max_length=25, verbose_name='\u6807\u7b7e\u7c7b\u578b', choices=[(b'job', '\u884c\u4e1a'), (b'interest', '\u5174\u8da3')])),
                ('tag_name', models.CharField(max_length=25, verbose_name='\u6807\u7b7e\u663e\u793a\u7684\u540d\u79f0')),
                ('helper_text', models.CharField(max_length=255, verbose_name='\u5e2e\u52a9\u4fe1\u606f')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick_name', models.CharField(help_text='\u7528\u6237\u6635\u79f0', max_length=63, verbose_name='\u6635\u79f0')),
                ('age', models.PositiveIntegerField(default=0, verbose_name='\u5e74\u9f84')),
                ('avatar', models.ImageField(upload_to=Profile.models.profile_avatar, verbose_name='\u5934\u50cf')),
                ('gender', models.CharField(max_length=1, verbose_name='\u6027\u522b', choices=[(b'm', '\u7537'), (b'f', '\u5973')])),
                ('birth_date', models.DateField(verbose_name='\u51fa\u751f\u65e5\u671f')),
                ('star_sign', models.CharField(max_length=25, verbose_name='\u661f\u5ea7', choices=[(b'Aries', '\u767d\u7f8a\u5ea7'), (b'Taurus', '\u91d1\u725b\u5ea7'), (b'Gemini', '\u53cc\u5b50\u5ea7'), (b'Cancer', '\u5de8\u87f9\u5ea7'), (b'Leo', '\u72ee\u5b50\u5ea7'), (b'Virgo', '\u5904\u5973\u5ea7'), (b'Libra', '\u5929\u79e4\u5ea7'), (b'Scorpio', '\u5929\u874e\u5ea7'), (b'Sagittarius', '\u5c04\u624b\u5ea7'), (b'Capricorn', '\u6469\u7faf\u5ea7'), (b'Aquarius', 's\u6c34\u74f6\u5ea7'), (b'Pisces', '\u53cc\u9c7c')])),
                ('district', models.CharField(max_length=255, verbose_name='\u5730\u533a')),
                ('signature', models.CharField(max_length=255, verbose_name='\u7b7e\u540d')),
                ('interest', models.ManyToManyField(related_name='profile_interest', verbose_name=b'\xe5\x85\xb4\xe8\xb6\xa3', to='Profile.ProfileTag')),
                ('job', models.ManyToManyField(related_name='profile_job', verbose_name=b'\xe8\xa1\x8c\xe4\xb8\x9a', to='Profile.ProfileTag')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u8be6\u60c5',
                'verbose_name_plural': '\u7528\u6237\u8be6\u60c5',
            },
        ),
    ]

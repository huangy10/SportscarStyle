# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_auto_20150930_0455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='star_sign',
            field=models.CharField(default=b'Aries', max_length=25, verbose_name='\u661f\u5ea7', choices=[(b'Aries', '\u767d\u7f8a\u5ea7'), (b'Taurus', '\u91d1\u725b\u5ea7'), (b'Gemini', '\u53cc\u5b50\u5ea7'), (b'Cancer', '\u5de8\u87f9\u5ea7'), (b'Leo', '\u72ee\u5b50\u5ea7'), (b'Virgo', '\u5904\u5973\u5ea7'), (b'Libra', '\u5929\u79e4\u5ea7'), (b'Scorpio', '\u5929\u874e\u5ea7'), (b'Sagittarius', '\u5c04\u624b\u5ea7'), (b'Capricorn', '\u6469\u7faf\u5ea7'), (b'Aquarius', 's\u6c34\u74f6\u5ea7'), (b'Pisces', '\u53cc\u9c7c')]),
        ),
    ]

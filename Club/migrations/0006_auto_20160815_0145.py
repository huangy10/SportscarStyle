# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0005_club_value_average'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubBillboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('version', models.IntegerField(verbose_name='\u7b2c*\u671f')),
                ('order', models.IntegerField(verbose_name='\u6392\u540d')),
                ('d_order', models.IntegerField(verbose_name='\u540d\u6b21\u53d8\u5316')),
                ('new_to_list', models.BooleanField(verbose_name='\u662f\u5426\u662f\u65b0\u4e0a\u699c')),
                ('scope', models.CharField(help_text='\u901a\u5e38\u662f\u57ce\u5e02\u7684\u540d\u79f0', max_length=50, verbose_name='\u6392\u5e8f\u8303\u56f4')),
                ('filter_type', models.CharField(max_length=20, verbose_name='\u6392\u5e8f\u7684\u7c7b\u578b', choices=[(b'total', b'\xe6\x80\xbb\xe4\xbb\xb7\xe6\x9c\x80\xe9\xab\x98'), (b'average', b'\xe5\x9d\x87\xe4\xbb\xb7\xe6\x9c\x80\xe9\xab\x98'), (b'members', b'\xe6\x88\x90\xe5\x91\x98\xe6\x95\xb0\xe9\x87\x8f'), (b'females', b'\xe7\xbe\x8e\xe5\xa5\xb3\xe6\x9c\x80\xe5\xa4\x9a')])),
                ('club', models.ForeignKey(verbose_name='\u4ff1\u4e50\u90e8', to='Club.Club')),
            ],
            options={
                'verbose_name': '\u6392\u884c\u699c',
                'verbose_name_plural': '\u6392\u884c\u699c',
            },
        ),
        migrations.AlterModelOptions(
            name='clubauthrequest',
            options={'verbose_name': '\u4ff1\u4e50\u90e8\u8ba4\u8bc1\u7533\u8bf7', 'verbose_name_plural': '\u4ff1\u4e50\u90e8\u8ba4\u8bc1\u7533\u8bf7'},
        ),
        migrations.AlterField(
            model_name='clubauthrequest',
            name='approve',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u6279\u51c6'),
        ),
        migrations.AlterField(
            model_name='clubauthrequest',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u5904\u7406'),
        ),
    ]

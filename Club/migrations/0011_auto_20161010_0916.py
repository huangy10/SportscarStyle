# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import custom.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0010_auto_20160828_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='deleted',
            field=custom.fields.BooleanField(default=False, verbose_name='\u4ff1\u4e50\u90e8\u662f\u5426\u88ab\u5220\u9664'),
        ),
        migrations.AlterField(
            model_name='club',
            name='identified',
            field=custom.fields.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8ba4\u8bc1'),
        ),
        migrations.AlterField(
            model_name='club',
            name='only_host_can_invite',
            field=custom.fields.BooleanField(default=False, verbose_name='\u53ea\u6709\u7fa4\u4e3b\u80fd\u591f\u9080\u8bf7'),
        ),
        migrations.AlterField(
            model_name='club',
            name='show_members_to_public',
            field=custom.fields.BooleanField(default=False, verbose_name='\u5bf9\u5916\u516c\u5e03\u6210\u5458\u4fe1\u606f'),
        ),
        migrations.AlterField(
            model_name='clubauthrequest',
            name='approve',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u6279\u51c6'),
        ),
        migrations.AlterField(
            model_name='clubauthrequest',
            name='checked',
            field=custom.fields.BooleanField(default=False, verbose_name='\u662f\u5426\u5df2\u7ecf\u5904\u7406'),
        ),
        migrations.AlterField(
            model_name='clubbillboard',
            name='new_to_list',
            field=custom.fields.BooleanField(verbose_name='\u662f\u5426\u662f\u65b0\u4e0a\u699c'),
        ),
        migrations.AlterField(
            model_name='clubjoining',
            name='always_on_top',
            field=custom.fields.BooleanField(default=False, verbose_name='\u7f6e\u9876\u804a\u5929'),
        ),
        migrations.AlterField(
            model_name='clubjoining',
            name='no_disturbing',
            field=custom.fields.BooleanField(default=False, verbose_name='\u6d88\u606f\u514d\u6253\u6270'),
        ),
        migrations.AlterField(
            model_name='clubjoining',
            name='show_nick_name',
            field=custom.fields.BooleanField(default=True, verbose_name='\u663e\u793a\u672c\u7fa4\u6210\u5458\u6635\u79f0'),
        ),
    ]

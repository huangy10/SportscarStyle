# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Status', '0002_auto_20160120_0754'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Activity', '0006_auto_20160205_0720'),
        ('News', '0003_auto_20160102_1357'),
        ('Club', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_type', models.CharField(max_length=100, choices=[(b'status_like', b'status_like'), (b'status_comment', b'your_status_are_commmented_by_others'), (b'status_comment_replied', b'your_comment_on_a_status_is_responsed_by_others'), (b'news_comment_replied', b'your commemnt_on_a_news_is_responsed_by_others'), (b'act_applied', b'some_one_applys_your_activity'), (b'act_approved', b'your_application_on_an_activity_is_approved'), (b'act_denied', b'your_application_on_an_activity_is_denied'), (b'act_full', b'one_of_your_activity_if_full_off_applicators'), (b'act_deleted', b'one_of_your_applied_activity_is_deleted'), (b'act_application_cancel', b'one_application_is_cancelled'), (b'act_invited', b'some_one_invite_you_for_an_activity'), (b'act_invitation_agreed', b'your_invitation_is_agreed'), (b'act_invitation_denied', b'your_invitation_is_denied'), (b'act_comment', b''), (b'act_comment_replied', b''), (b'auth_car_approved', b'your_application_for_sportscar_identification_is_approved'), (b'auth_car_denied', b'your_application_for_sportscar_identification_is_denied'), (b'auth_club_approved', b'your_application_for_club_identification_is_approved'), (b'auth_club_denied', b'your_application_for_club_identification_is_denied'), (b'auth_act_approved', b''), (b'auth_act_denied', b''), (b'relation_follow', b'')])),
                ('message_body', models.CharField(max_length=255, verbose_name=b'\xe6\xb6\x88\xe6\x81\xaf\xe5\x86\x85\xe5\xae\xb9(Optional)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('read', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe8\xaf\xbb')),
                ('flag', models.BooleanField(default=False, verbose_name=b'\xe4\xbf\x9d\xe7\x95\x99\xe5\xad\x97\xe6\xae\xb5')),
                ('related_act', models.ForeignKey(related_name='+', to='Activity.Activity', null=True)),
                ('related_act_comment', models.ForeignKey(related_name='+', to='Activity.ActivityComment', null=True)),
                ('related_act_invite', models.ForeignKey(related_name='+', to='Activity.ActivityInvitation', null=True)),
                ('related_act_join', models.ForeignKey(related_name='+', to='Activity.ActivityJoin', null=True)),
                ('related_club', models.ForeignKey(related_name='+', to='Club.Club', null=True)),
                ('related_news', models.ForeignKey(related_name='+', to='News.News', null=True)),
                ('related_news_comment', models.ForeignKey(related_name='+', to='News.NewsComment', null=True)),
                ('related_status', models.ForeignKey(related_name='+', to='Status.Status', null=True)),
                ('related_status_comment', models.ForeignKey(related_name='+', to='Status.StatusComment', null=True)),
                ('related_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('target', models.ForeignKey(verbose_name=b'\xe7\x9b\xae\xe6\xa0\x87\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': '\u6d88\u606f',
                'verbose_name_plural': '\u6d88\u606f',
            },
        ),
    ]

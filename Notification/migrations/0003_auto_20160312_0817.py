# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sportscar', '0006_auto_20160302_0829'),
        ('Notification', '0002_auto_20160307_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='related_own',
            field=models.ForeignKey(related_name='+', to='Sportscar.SportCarOwnership', null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message_type',
            field=models.CharField(max_length=100, choices=[(b'status_like', b'status_like'), (b'status_comment', b'your_status_are_commmented_by_others'), (b'status_comment_replied', b'your_comment_on_a_status_is_responsed_by_others'), (b'status_inform', b''), (b'news_comment_replied', b'your commemnt_on_a_news_is_responsed_by_others'), (b'act_applied', b'some_one_applys_your_activity'), (b'act_approved', b'your_application_on_an_activity_is_approved'), (b'act_denied', b'your_application_on_an_activity_is_denied'), (b'act_full', b'one_of_your_activity_if_full_off_applicators'), (b'act_deleted', b'one_of_your_applied_activity_is_deleted'), (b'act_application_cancel', b'one_application_is_cancelled'), (b'act_invited', b'some_one_invite_you_for_an_activity'), (b'act_invitation_agreed', b'your_invitation_is_agreed'), (b'act_invitation_denied', b'your_invitation_is_denied'), (b'act_comment', b''), (b'act_comment_replied', b''), (b'auth_car_approved', b'your_application_for_sportscar_identification_is_approved'), (b'auth_car_denied', b'your_application_for_sportscar_identification_is_denied'), (b'auth_club_approved', b'your_application_for_club_identification_is_approved'), (b'auth_club_denied', b'your_application_for_club_identification_is_denied'), (b'auth_act_approved', b''), (b'auth_act_denied', b''), (b'relation_follow', b''), (b'chat', b'')]),
        ),
    ]

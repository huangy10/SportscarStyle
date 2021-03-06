import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from .models import SettingCenter, Suggestion

# Create your tests here.


class SettingsTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username='15201525181')
        user.set_password('test_password')
        user.save()
        self.user = user
        self.another_user = get_user_model().objects.create(username='13573561235')

    def authenticate(self):
        self.client.post(reverse('account:login'), data=dict(
            username='15201525181',
            password='test_password'
        ))

    def test_setting_center_auto_creation(self):
        self.assertIsNotNone(self.user.setting_center)

    def test_backup_settings(self):
        self.authenticate()
        response = self.client.post(reverse('settings:settings'), data=dict(
            notification_accept='YES',
            notification_sound='YES',
            notification_shake='YES',
            location_visible_to='all',
            accept_invitation="all",
            show_on_map="YES",
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        setting_center = SettingCenter.objects.get(user=self.user)

    def test_get_settings(self):
        self.authenticate()
        response = self.client.get(reverse('settings:settings'))
        response_data = json.loads(response.content)

        self.assertEqual(response_data['settings'],
                         dict(notification_accept=True, notification_sound=True, notification_shake=True,
                              location_visible_to='all', blacklist=None, accept_invitation="all",
                              show_on_map=True))

    # def test_remove_black_list(self):
    #     self.user.setting_center.blacklist.add(self.another_user)
    #     self.authenticate()
    #     response = self.client.post(reverse('settings:settings'), data=dict(
    #         notification_accept='YES',
    #         notification_sound='YES',
    #         notification_shake='YES',
    #         location_visible_to='all',
    #         accept_invitation="all",
    #         show_on_map="YES",
    #         blacklist=json.dumps({'remove': [self.another_user.id]})
    #     ))
    #     response_data = json.loads(response.content)
    #     self.assertTrue(response_data['success'])
    #     setting_center = self.user.setting_center
    #     self.assertEqual(setting_center.blacklist.all().count(), 0)

    def test_give_suggestions(self):
        self.authenticate()
        self.client.post(reverse('settings:suggestions'), data=dict(
            content='test_content'
        ))
        self.assertEqual(len(Suggestion.objects.all()), 1)

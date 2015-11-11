import datetime
import json
import random
import os

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings

from .models import Activity, ActivityComment
from Club.models import Club
# Create your tests here.


class ActivityViewTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username='15201525181')
        user.set_password('test_password')
        user.save()
        self.user = user

    def authenticate(self):
        self.client.post(reverse('account:login'), data=dict(
            username='15201525181',
            password='test_password'
        ))

    def test_activity_create(self):
        self.authenticate()
        poster = open(os.path.join(settings.BASE_DIR, 'media', 'tests', 'test.png'))
        response = self.client.post(reverse('activity:create'), data=dict(
            name='test activity',
            description='description',
            max_attend=10,
            start_at=(timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S %Z'),
            end_at=(timezone.now() + datetime.timedelta(days=12)).strftime('%Y-%m-%d %H:%M:%S %Z'),
            location=json.dumps(dict(lat=30, lon=120, description='test location')),
            poster=poster
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_activity_create_with_club_limit(self):
        self.authenticate()
        club = Club.objects.create(name='test_club', host=self.user, logo='meida/tests/test.png', description='test')
        poster = open(os.path.join(settings.BASE_DIR, 'media', 'tests', 'test.png'))
        response = self.client.post(reverse('activity:create'), data=dict(
            name='test activity',
            description='description',
            max_attend=10,
            start_at=(timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S %Z'),
            end_at=(timezone.now() + datetime.timedelta(days=12)).strftime('%Y-%m-%d %H:%M:%S %Z'),
            location=json.dumps(dict(lat=30, lon=120, description='test location')),
            club_limit=club.id,
            poster=poster
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        act = Activity.objects.first()
        self.assertEqual(act.allowed_club.id, club.id)

    def test_activity_create_with_inform_of(self):
        self.authenticate()
        users = []
        user_num = random.randint(1, 20)
        for i in range(user_num):
            users.append(get_user_model().objects.create(username='another_user_%s' % i))
        poster = open(os.path.join(settings.BASE_DIR, 'media', 'tests', 'test.png'))
        response = self.client.post(reverse('activity:create'), data=dict(
            name='test activity',
            description='description',
            max_attend=10,
            start_at=(timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S %Z'),
            end_at=(timezone.now() + datetime.timedelta(days=12)).strftime('%Y-%m-%d %H:%M:%S %Z'),
            location=json.dumps(dict(lat=30, lon=120, description='test location')),
            inform_of=json.dumps(map(lambda x: x.id, users)),
            poster=poster
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        act = Activity.objects.first()
        self.assertEqual(len(act.inform_of.all()), user_num)


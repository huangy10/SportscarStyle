# coding=utf-8
import datetime
import json
import random
import os

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.gis.geos import Point

from .models import Activity, ActivityComment, ActivityJoin
from Club.models import Club
from Location.models import Location
# Create your tests here.


class ActivityViewTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username='15201525181')
        user.set_password('test_password')
        user.save()
        self.user = user
        self.activity = Activity.objects.create(
            name="test_activity",
            description="test",
            max_attend=10,
            start_at=timezone.now() + datetime.timedelta(days=1),
            end_at=timezone.now() + datetime.timedelta(days=2),
            allowed_club=None,
            poster="/media/tests/test.png",
            location=Location.objects.create(location=Point(30, 120), description='test')
        )

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
            start_at=(timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
            end_at=(timezone.now() + datetime.timedelta(days=12)).strftime('%Y-%m-%d %H:%M:%S'),
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
            start_at=(timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
            end_at=(timezone.now() + datetime.timedelta(days=12)).strftime('%Y-%m-%d %H:%M:%S'),
            location=json.dumps(dict(lat=30, lon=120, description='test location')),
            club_limit=club.id,
            poster=poster
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        act = Activity.objects.order_by('-created_at').first()
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
            start_at=(timezone.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
            end_at=(timezone.now() + datetime.timedelta(days=12)).strftime('%Y-%m-%d %H:%M:%S'),
            location=json.dumps(dict(lat=30, lon=120, description='test location')),
            inform_of=json.dumps(map(lambda x: x.id, users)),
            poster=poster
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        act = Activity.objects.order_by('-created_at').first()
        self.assertEqual(len(act.inform_of.all()), user_num)

    def test_activity_check_detail(self):
        self.authenticate()
        response = self.client.get(reverse('activity:detail', args=(self.activity.id, )))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(response_data['data'], dict(
            name=self.activity.name,
            description=self.activity.description,
            max_attend=self.activity.max_attend,
            start_at=self.activity.start_at.strftime('%Y-%m-%d %H:%M:%S'),
            end_at=self.activity.end_at.strftime('%Y-%m-%d %H:%M:%S'),
            poster=self.activity.poster.url,
            location=dict(lat=self.activity.location.location.x,
                          lon=self.activity.location.location.y,
                          description=self.activity.location.description),
            apply_list=[],
        ))

    def test_activity_check_detail_with_appliers(self):
        another_user = get_user_model().objects.create(username='new_user')
        ActivityJoin.objects.create(user=another_user, activity=self.activity)
        self.authenticate()
        response = self.client.get(reverse('activity:detail', args=(self.activity.id, )))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(response_data['data'], dict(
            name=self.activity.name,
            description=self.activity.description,
            max_attend=self.activity.max_attend,
            start_at=self.activity.start_at.strftime('%Y-%m-%d %H:%M:%S'),
            end_at=self.activity.end_at.strftime('%Y-%m-%d %H:%M:%S'),
            poster=self.activity.poster.url,
            location=dict(lat=self.activity.location.location.x,
                          lon=self.activity.location.location.y,
                          description=self.activity.location.description),
            apply_list=[dict(
                approved=False,
                user=dict(
                    id=another_user.id,
                    avatar=another_user.profile.avatar.url,
                    avatar_car=None)
            ), ],
        ))

    def test_activity_post_comment(self):
        self.authenticate()
        response = self.client.post(reverse('activity:comment', args=(self.activity.id, )), data=dict(
            content='test content',
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(ActivityComment.objects.all().count(), 1)

    def test_activity_post_commnet_with_response_to_previous_commnet(self):
        self.authenticate()
        pre_comment = ActivityComment.objects.create(
            user=get_user_model().objects.create(username='another_new_user'),
            activity=self.activity, image=None,
            content='test',
        )
        response = self.client.post(reverse('activity:comment', args=(self.activity.id, )), data=dict(
            content='test content',
            response_to=pre_comment.id
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(ActivityComment.objects.all().count(), 2)
        comment = ActivityComment.objects.order_by('-created_at').first()
        self.assertEqual(comment.response_to.id, pre_comment.id)

    def test_activity_post_comment_with_inform_of(self):
        """ 在这个测试中加入@别人的效果
        """
        self.authenticate()
        users = []
        for i in range(3):
            users.append(get_user_model().objects.create(username='new_user_%s' % i))
        response = self.client.post(reverse('activity:comment', args=(self.activity.id, )), data=dict(
            content='test content',
            inform_of=json.dumps([user.id for user in users])
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        comment = ActivityComment.objects.get(id=response_data['id'])
        self.assertEqual(comment.inform_of.all().count(), 3)




# coding=utf-8
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import ClubJoining, Club
# Create your tests here.


class ClubModelTest(TestCase):
    """ 测试俱乐部模型系统功能
    """

    def setUp(self):
        self.default_user = get_user_model().objects.create(username='test_user')
        self.default_club = Club.objects.create(name='test club',
                                                host=self.default_user,
                                                logo='/media/tests/test.png',
                                                description='test club')

    def test_host_auto_join(self):
        """ 测试：作为俱乐部的创始人，应当始终被自动加入俱乐部
        """
        self.assertTrue(ClubJoining.objects.filter(user=self.default_user,
                                                   club=self.default_club).exists())


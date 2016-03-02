# coding=utf-8
import os
import datetime
import json
import random

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.gis.geos import Point

from .models import Status, StatusComment, StatusLikeThrough
from Location.models import Location
from Sportscar.models import Sportscar, Manufacturer
from Club.models import Club, ClubJoining

# Create your tests here.


class StatusViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        new_user = get_user_model().objects.create(username='15201525181')
        new_user.set_password('huang9040601')
        new_user.save()
        self.default_user = new_user
        self.guest_user = get_user_model().objects.create(username='guest user')
        self.default_manufacturer = Manufacturer.objects.create(
            name=u'宝马',
            name_english=u'BMW',
        )
        self.car1 = Sportscar.objects.create(
            name=u'Mini Cooper',
            name_english=u'Mini Cooper',
            price='300,000',
            seats=4,
            fuel_consumption=1,
            displacement=1.5,
            release_date=datetime.date(year=2000, month=1, day=1),
            logo=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
            image=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
            engine=u'4.5L 605马力V8',
            transmission=u'2门2座硬顶跑车',
            max_speed=u'325 km/h',
            zeroTo60='3s',
            manufacturer=self.default_manufacturer
        )
        self.default_location = Location.objects.create(
            location=Point(120, 30),
            description='test location',
        )
        self.default_status = Status.objects.\
            create(user=self.default_user,
                   image1=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
                   content='status content',
                   location=self.default_location,
                   car=self.car1)

    def authenticate(self):
        self.client.post(reverse('account:login'), data=dict(username='15201525181', password='huang9040601'))

    def create_status(self, num=0):
        for _ in range(num):
            Status.objects.create(user=self.default_user,
                                  image=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
                                  content='status content',
                                  location=self.default_location,
                                  car=self.car1)

    def test_status_list_access_more(self):
        """ 测试状态列表首页获取是否正常
        """
        self.authenticate()
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertTrue(response_data["success"])
        self.assertEqual(len(response_data["data"]), 1)
        status = self.default_status
        status_dict = status.dict_description()
        status_dict["comment_num"] = 0
        status_dict["like_num"] = 0
        self.assertEqual(response_data["data"][0], status_dict)

    def test_stauts_list_access_latest(self):
        """ 测试状态列表首页获取是否正常
        """
        self.authenticate()
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertTrue(response_data["success"])
        self.assertEqual(len(response_data["data"]), 1)

    def test_status_list_access_with_avatar_club(self):
        """ 在setUp创建的数据集里面，没有引入签名俱乐部，这个测试给默认用户加入签名俱乐部
        """
        # 首先创建一个俱乐部
        club = Club.objects.create(name='test club', host=self.default_user,
                                   logo=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
                                   description='test club')
        # 将这个俱乐部设置为default_user的avatar_club
        self.default_user.profile.avatar_club = club
        self.default_user.profile.save()
        # 然后进行访问
        self.authenticate()
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(len(response_data["data"]), 1)
        status = self.default_status
        status_dict = status.dict_description()
        status_dict["comment_num"] = 0
        status_dict["like_num"] = 0
        self.assertEqual(response_data["data"][0], status_dict)

    def test_status_list_comment_num(self):
        """ 测试返回的评论数量是否正确
        """
        random_comment_num = random.randint(1, 20)
        for _ in range(random_comment_num):
            StatusComment.objects.create(status=self.default_status,
                                         user=self.guest_user,
                                         image='/media/tests/test.png',
                                         content='content')
        self.authenticate()
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data["data"]), 1)
        status = self.default_status
        status_dict = status.dict_description()
        status_dict["comment_num"] = random_comment_num
        status_dict["like_num"] = 0
        self.assertEqual(response_data["data"][0], status_dict)

    def test_status_list_like_num(self):
        """ 测试点赞人数是否正确
        """
        random_like_num = random.randint(0, 20)
        for i in range(random_like_num):
            user = get_user_model().objects.create(username=str(i))
            StatusLikeThrough.objects.create(user=user, status=self.default_status)
        self.authenticate()
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(len(response_data["data"]), 1)
        status = self.default_status
        status_dict = status.dict_description()
        status_dict["comment_num"] = 0
        status_dict["like_num"] = random_like_num
        self.assertEqual(response_data["data"][0], status_dict)

    def test_status_post(self):
        """ 测试发布状态的接口是否工作正常
        """
        self.authenticate()
        image = open(os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'))
        response = self.client.post(reverse('status:post_status'), data=dict(
            image1=image,
            user_id=self.default_user.id,
            car_id=self.car1.id,
            lat=30,
            lon=120,
            location_description='test location',
            content='test_content',
        ))
        image.close()
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIsNotNone(response_data.get("statusID", None))

    def test_status_post_using_mulit_images(self):
        """ 上传多张图片
        """
        self.authenticate()
        image = open(os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'))
        image2 = open(os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'))
        response = self.client.post(reverse('status:post_status'), data=dict(
            image1=image,
            image2=image2,
            user_id=self.default_user.id,
            car_id=self.car1.id,
            lat=30,
            lon=120,
            location_description='test location',
            content='test_content',
        ))
        image.close()
        image2.close()
        response_data = json.loads(response.content)
        print response_data
        self.assertTrue(response_data["success"])

    def test_status_post_with_invalid_user_id(self):
        self.authenticate()
        image = open(os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'))
        response = self.client.post(reverse('status:post_status'), data=dict(
            image=image,
            user_id=1000,
            car_id=self.car1.id,
            lat=30,
            lon=120,
            location_description='test location',
            content='test_content',
        ))
        image.close()
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def test_status_post_with_invalid_car_id(self):
        self.authenticate()
        image = open(os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'))
        response = self.client.post(reverse('status:post_status'), data=dict(
            image=image,
            user_id=self.default_user.id,
            car_id=10000,
            lat=30,
            lon=120,
            location_description='test location',
            content='test_content',
        ))
        image.close()
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def create_comments(self, num=10, user=None, status=None):
        """ 批量创建供测试的评论
         :return 如果只要求创建一条评论，那么返回评论本身，否则返回评论组成的数组
        """
        result = []
        if user is None:
            user = self.default_user
        if status is None:
            status = self.default_status
        for _ in range(num):
            result.append(
                StatusComment.objects.create(
                    user=user,
                    image='media/tests/test.png',
                    content='test content',
                    status=status,
                )
            )
        if num == 1:
            return result[0]
        else:
            return result

    def test_status_comment_list_more(self):
        self.authenticate()
        another_user = get_user_model().objects.create(username='another_user')
        comment = self.create_comments(num=1, user=another_user)
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_comments', args=(self.default_status.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(
            response_data,
            dict(
                success=True,
                comments=[comment.dict_description()]
            )
        )

    def test_status_comment_list_latest(self):
        self.authenticate()
        another_user = get_user_model().objects.create(username='another_user')
        comment = self.create_comments(num=1, user=another_user)
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_comments', args=(self.default_status.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(
            response_data,
            dict(
                success=True,
                comments=[comment.dict_description()]
            )
        )

    def test_status_comments_list_with_limit(self):
        self.authenticate()
        another_user = get_user_model().objects.create(username='another_user')
        self.create_comments(num=20, user=another_user)
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('status:status_comments', args=(self.default_status.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['comments']), 10)

    def test_status_post_comment(self):
        self.authenticate()
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
            content='test content',
            image=open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))

    def test_status_post_comment_text_only(self):
        self.authenticate()
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
            content='test content',
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))
        comment = StatusComment.objects.all()[0]
        self.assertEqual(comment.status.id, self.default_status.id)

    def test_status_post_comment_image_only(self):
        self.authenticate()
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
            image=open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))

    def test_status_post_comment_without_login(self):
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
            content='test content',
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, message='You need to login first', code='1402'))

    def test_status_post_comment_without_valid_content(self):
        self.authenticate()
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False,
                                             code='4003', message=u'No valid content found for the comment'))

    def test_status_post_comment_with_response_to(self):
        self.authenticate()
        comment = self.create_comments(num=1)
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
            content='test content',
            response_to=comment.id
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))
        new_comment = StatusComment.objects.all().order_by('-created_at').first()
        self.assertEqual(new_comment.response_to.id, comment.id)

    def test_status_post_comment_with_inform_of(self):
        self.authenticate()
        another_user = get_user_model().objects.create(username='another_username')
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
            content='test content',
            inform_of=json.dumps([another_user.id, ])
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))
        new_comment = StatusComment.objects.all().order_by('-created_at').first()
        self.assertEqual(new_comment.inform_of.all()[0].id, another_user.id)

    def test_status_post_comment_with_multi_inform_of(self):
        self.authenticate()
        users = []
        for i in range(10):
            users.append(get_user_model().objects.create(username=('test_username_%s' % i)))
        users_id = map(lambda x: x.id, users)
        response = self.client.post(reverse('status:post_comments', args=(self.default_status.id, )), data=dict(
            content='test content',
            inform_of=json.dumps(users_id)
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))
        new_comment = StatusComment.objects.all().order_by('-created_at').first()
        self.assertEqual(len(new_comment.inform_of.all()), 10)

    def test_status_operation_like(self):
        self.authenticate()
        response = self.client.post(reverse('status:status_operation', args=(self.default_status.id, )), data=dict(
            op_type='like'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(
            success=True, like_state=True
        ))
        self.assertTrue(StatusLikeThrough.objects.filter(user=self.default_user, status=self.default_status).exists())

    def test_status_operation_like_toggle(self):
        self.authenticate()
        self.client.post(reverse('status:status_operation', args=(self.default_status.id, )), data=dict(
            op_type='like'
        ))
        response = self.client.post(reverse('status:status_operation', args=(self.default_status.id, )), data=dict(
            op_type='like'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(
            success=True, like_state=False
        ))
        self.assertFalse(StatusLikeThrough.objects.filter(user=self.default_user, status=self.default_status).exists())

    def test_status_operation_with_invalid_op_type(self):
        self.authenticate()
        response = self.client.post(reverse('status:status_operation', args=(self.default_status.id, )), data=dict(
            op_type='invalid op_type'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='4004', message='Operation not defined'))

    def test_status_operation_without_op_type(self):
        self.authenticate()
        response = self.client.post(reverse('status:status_operation', args=(self.default_status.id, )), data=dict(
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='4300', message='No valid operation type param found.'))

    def test_status_operation_with_invalid_status_id(self):
        self.authenticate()
        invalid_id = 1000
        while invalid_id == self.default_status.id:
            invalid_id = random.randint(0, 1000)
        response = self.client.post(reverse('status:status_operation', args=(invalid_id, )), data=dict(
            op_type='like'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='4002', message='Status not found.'))

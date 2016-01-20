# coding=utf-8
import os
import json
import datetime

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone

from .models import News, NewsComment, NewsLikeThrough
# Create your tests here.


class NewsViewsTest(TestCase):

    def setUp(self):
        self.news1 = News.objects.create(
            cover=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
            title='title',
            content='content',
            shared_times=10
        )
        self.default_user = get_user_model().objects.create(username='15201525181')
        self.default_user.set_password('huang9040601')
        self.default_user.save()
        NewsLikeThrough.objects.create(user=self.default_user, news=self.news1)
        self.client = Client()

    def authenticate(self):
        self.client.post(reverse('account:login'), data=dict(username='15201525181', password='huang9040601'))

    def test_news_list_more(self):
        self.authenticate()
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:news_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertEqual(len(response_data["news"]), 1)

    def test_news_list_latest(self):
        self.authenticate()
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:news_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertEqual(len(response_data["news"]), 1)

    def test_news_list_with_invalid_operation_type(self):
        self.authenticate()
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:news_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='invalid',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(
            success=False, code='3400', message='invalid op_type'
        ))

    def test_news_list_limit(self):
        new_news = self.news1
        for _ in range(20):
            new_news.id = None
            new_news.save()
        self.authenticate()
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:news_list'), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['news']), 10)

    def test_news_detail(self):
        self.authenticate()
        response = self.client.get(reverse('news:news_detail', args=(self.news1.id, )))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True, recent_like=self.default_user.profile.nick_name))

    def test_news_detail_no_recent_like(self):
        self.authenticate()
        news2 = News.objects.create(
            cover=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
            title='title',
            content='content',
            shared_times=10
        )
        response = self.client.get(reverse('news:news_detail', args=(news2.id, )))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True, recent_like=''))

    def test_news_detail_with_invalid_id(self):
        self.authenticate()
        response = self.client.get(reverse('news:news_detail', args=(1000, )))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='3000', message='News not found.'))

    def create_comments(self, num=10):
        """ Create a lot of comments for test
        """
        result = []
        for _ in range(num):
            result.append(
                NewsComment.objects.create(user=self.default_user,
                                           image=os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'),
                                           content='test content',
                                           news=self.news1,
                                           created_at=timezone.now())
            )
        return result

    def test_news_get_comments_more(self):
        self.authenticate()
        comment = self.create_comments(num=1)[0]
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:comments_list', args=(self.news1.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertTrue(response_data["success"])

    def test_news_get_comments_latest(self):
        self.authenticate()
        comment = self.create_comments(num=1)[0]
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:comments_list', args=(self.news1.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertTrue(response_data["success"])


    def test_news_get_comments_with_limit(self):
        self.authenticate()
        self.create_comments(20)
        comment = self.create_comments(num=1)[0]
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:comments_list', args=(self.news1.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['comments']), 10)

    def test_news_without_login(self):
        self.create_comments(20)
        comment = self.create_comments(num=1)[0]
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('news:comments_list', args=(self.news1.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, message='You need to login first', code='1402'))

    def test_news_post_comment_without_login(self):
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )), data=dict(
            content='test content'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, message='You need to login first', code='1402'))

    def test_news_post_comment(self):
        self.authenticate()
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )), data=dict(
            content='test content'
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIsNotNone(response_data.get("id", None))
        im = open(os.path.join(settings.MEDIA_ROOT, 'tests', 'test.png'))
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )), data=dict(
            image=im
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIsNotNone(response_data.get("id", None))
        im.close()

    def test_news_post_comment_response_to_former_comment(self):
        self.authenticate()
        comment = self.create_comments(1)[0]
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )), data=dict(
            content='test content',
            response_to=comment.id
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIsNotNone(response_data.get("id", None))
        new_comment = NewsComment.objects.all().order_by('-created_at').first()
        self.assertEqual(new_comment.news.id, self.news1.id)
        self.assertEqual(new_comment.response_to.id, comment.id)

    def test_news_post_comment_without_valid_content(self):
        self.authenticate()
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )))
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         dict(success=False, code='3003', message=u'No valid content found for the comment'))

    def test_news_post_comment_with_empty_content(self):
        self.authenticate()
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )), data=dict(
            content=''
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         dict(success=False, code='3003', message=u'No valid content found for the comment'))

    def test_news_post_comment_with_inform_of(self):
        self.authenticate()
        comment = self.create_comments(1)[0]
        another_user = get_user_model().objects.create(username='another_test_user_abc')
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )), data=dict(
            content='test content',
            response_to=comment.id,
            inform_of=json.dumps([another_user.id]),
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIsNotNone(response_data.get("id", None))
        new_comment = NewsComment.objects.all().order_by('-created_at').first()
        self.assertEqual(new_comment.news.id, self.news1.id)
        self.assertEqual(new_comment.response_to.id, comment.id)

    def test_news_post_comment_with_multi_inform_of(self):
        self.authenticate()
        comment = self.create_comments(1)[0]
        users = []
        for i in range(10):
            users.append(get_user_model().objects.create(username=('test_username_%s' % i)))
        users_id = map(lambda x: x.id, users)
        response = self.client.post(reverse('news:post_comment', args=(self.news1.id, )), data=dict(
            content='test content',
            response_to=comment.id,
            inform_of=json.dumps(users_id),
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data["success"])
        self.assertIsNotNone(response_data.get("id", None))
        new_comment = NewsComment.objects.all().order_by('-created_at').first()
        self.assertEqual(new_comment.news.id, self.news1.id)
        self.assertEqual(new_comment.response_to.id, comment.id)

    def test_news_operation_like(self):
        self.authenticate()
        response = self.client.post(reverse('news:news_operation', args=(self.news1.id, )), data=dict(
            op_type='like',
        ))
        response_data = json.loads(response.content)
        # 注意：在setup函数里面我们已经加入了default_user到news1的like，所以这里返回的like_state应是False
        self.assertEqual(response_data, dict(
            success=True, like_state=False
        ))
        self.assertFalse(NewsLikeThrough.objects.filter(user=self.default_user, news=self.news1).exists())

    def test_news_operation_like_toggle(self):
        self.authenticate()
        self.client.post(reverse('news:news_operation', args=(self.news1.id, )), data=dict(
            op_type='like',
        ))
        response = self.client.post(reverse('news:news_operation', args=(self.news1.id, )), data=dict(
            op_type='like',
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(
            success=True, like_state=True
        ))
        self.assertTrue(NewsLikeThrough.objects.filter(user=self.default_user, news=self.news1).exists())

    def test_news_operation_invalid_op_type(self):
        self.authenticate()
        response = self.client.post(reverse('news:news_operation', args=(self.news1.id, )), data=dict(
            op_type='invalid op_type',
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='3004', message='Operation not defined'))

    def test_news_operation_without_op_type(self):
        self.authenticate()
        response = self.client.post(reverse('news:news_operation', args=(self.news1.id, )))
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         dict(success=False, code='3301', message='No valid operation type param found.'))

    def test_news_operation_with_invalid_news_id(self):
        self.authenticate()
        response = self.client.post(reverse('news:news_operation', args=(1000, )), data=dict(
            op_type='like',
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         dict(success=False, code='3001', message='News not found.'))


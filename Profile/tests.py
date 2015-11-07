# coding=utf-8
import json
import random
import os
import datetime

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.files import File
from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils import timezone

from .models import AuthenticationCode, UserProfile, UserFollow
from .utils import create_random_code, star_sign_from_date
from Club.models import Club
from Sportscar.models import Sportscar, Manufacturer, SportCarOwnership
from Status.models import Status
from Location.models import Location

# Create your tests here.


class ProfileModelTest(TestCase):
    """ We will fullly test all the model in the Profile.models in this test class
    """
    def setUp(self):
        self.client = Client()
        self.default_user = get_user_model().objects.create(username='15201525181')
        self.default_user.set_password('test_password')
        self.default_user.save()

    def test_profile_auto_creation(self):
        self.assertIsNotNone(self.default_user.profile)

    def test_profile_age_auto_calculation(self):
        self.default_user.profile.birth_date = datetime.date(year=2000, month=1, day=1)
        self.assertEqual(self.default_user.profile.age, 15)
        # test with leap year
        self.default_user.profile.birth_date = datetime.date(year=2000, month=2, day=29)
        self.assertEqual(self.default_user.profile.age, 15)
        # test with birthday
        today = datetime.datetime.today()
        self.default_user.profile.birth_date = datetime.date(year=2000, month=today.month, day=today.day)
        self.assertEqual(self.default_user.profile.age, 15)
        next_day = today + datetime.timedelta(seconds=3600*24)
        self.default_user.profile.birth_date = datetime.date(year=2000, month=next_day.month, day=next_day.day)
        self.assertEqual(self.default_user.profile.age, 14)


class ProfileUtilityTest(TestCase):

    def test_random_code_length(self):
        code = create_random_code()
        self.assertEqual(len(code), 6)

    def test_star_sign_from_date(self):
        today = datetime.date(year=1992, month=1, day=30)
        sign = star_sign_from_date(today)
        self.assertEqual(sign, 'Aquarius')


class ProfileViewTest(TestCase):
    """ We will fully test all the views in the Profile.views in this test class
    """
    def setUp(self):
        self.client = Client()
        self.default_user = get_user_model().objects.create(username='15201525181')
        self.default_user.set_password('test_password')
        self.default_user.save()

    # def test_send_code(self):
    #     """In this test, we make sure that the sms authentication systems works fine
    #     """
    #     response = self.client.post('/account/sendcode', data=dict(phoen_num='15201525181'))
    #     response_data = json.loads(response.content)
    #     self.assertEqual(response_data, dict(success=True))

    def test_login(self):
        """ Test the accessibility of /account/login
        """
        response = self.client.post('/account/login', data=dict(username='15201525181', password='test_password'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))

    def test_login_with_invalid_username(self):
        response = self.client.post('/account/login', data=dict(username='invalid_username', password='test_password'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False,
                                             message='invalid username',
                                             code='1000'))

    def test_login_with_wrong_password(self):
        response = self.client.post('/account/login', data=dict(username='15201525181', password='wrong_password'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False,
                                             message='password incorrect',
                                             code='1001'))

    def test_register(self):
        code = create_random_code()
        phone = '18570353219'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='new_password',
                         auth_code=code)
        response = self.client.post('/account/register', data=post_data)
        response_data = json.loads(response.content)
        self.assertTrue(response_data.get('success', False))

    def test_register_with_password_not_consistent(self):
        code = create_random_code()
        phone = '18570353219'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='another_password',
                         auth_code=code)
        response = self.client.post('/account/register', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='1002',
                                             password2=[u"The two password fields didn't match."]))

    def test_register_with_invalid_auth_code(self):
        code = "111111"
        phone = '18570353219'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='new_password',
                         auth_code='000000')
        response = self.client.post('/account/register', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='1002',
                                             auth_code=[u"invalid code"]))

    def test_register_with_password_too_short(self):
        code = create_random_code()
        phone = '18570353219'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='short',
                         password2='short',
                         auth_code=code)
        response = self.client.post('/account/register', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='1002',
                                             password2=[u"password too short"]))

    def test_register_auto_set_used_code_to_inactive(self):
        code = create_random_code()
        phone = '18570353219'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='new_password',
                         auth_code=code)
        self.client.post('/account/register', data=post_data)
        record = AuthenticationCode.objects.get(phone_num=phone, code=code)
        self.assertFalse(record.is_active)

    def test_reset_password(self):
        code = create_random_code()
        phone = '15201525181'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='new_password',
                         auth_code=code)
        response = self.client.post('/account/reset', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))

    def test_reset_password_invalid_username(self):
        code = create_random_code()
        phone = '15201525182'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='new_password',
                         auth_code=code)
        response = self.client.post('/account/reset', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, username=['invalid username']))

    def test_reset_password_mismatch(self):
        code = create_random_code()
        phone = '15201525181'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='password_mismatch',
                         auth_code=code)
        response = self.client.post('/account/reset', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, password2=[u'password mismatch.']))

    def test_reset_password_too_short(self):
        code = create_random_code()
        phone = '15201525181'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='short',
                         password2='short',
                         auth_code=code)
        response = self.client.post('/account/reset', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, password2=[u'password too short']))

    def test_reset_password_invalid_code(self):
        code = '000000'
        phone = '15201525181'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='new_password',
                         auth_code='111111')
        response = self.client.post('/account/reset', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, auth_code=[u'invalid code']))

    def test_reset_password_code_auto_to_invalid(self):
        code = create_random_code()
        phone = '15201525181'
        AuthenticationCode.objects.create(phone_num=phone, code=code)
        post_data = dict(username=phone,
                         password1='new_password',
                         password2='new_password',
                         auth_code=code)
        self.client.post('/account/reset', data=post_data)
        record = AuthenticationCode.objects.get(phone_num=phone, code=code)
        self.assertFalse(record.is_active)

    def test_create_profile(self):
        # login first
        self.client.post('/account/login', data=dict(username='15201525181', password='test_password'))
        #
        gender = random.choice(['m', 'f'])
        post_data = dict(nick_name='test_nick_name',
                         gender=gender,
                         birth_date='1992-01-30')
        response = self.client.post('/account/profile', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))
        profile = UserProfile.objects.get(user=self.default_user)
        self.assertEqual(profile.nick_name, 'test_nick_name')
        self.assertEqual(profile.gender, gender)
        self.assertEqual(profile.birth_date, datetime.date(year=1992, month=1, day=30))
        self.assertEqual(profile.star_sign, 'Aquarius')

    def test_create_profile_without_login(self):
        gender = random.choice(['m', 'f'])
        post_data = dict(nick_name='test_nick_name',
                         gender=gender,
                         birth_date='1992-01-30')
        response = self.client.post('/account/profile', data=post_data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, message='You need to login first',
                                             code='1402'))


class PersonalViewTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username='15201525181')
        user.set_password('test_password')
        user.save()
        self.default_user = user

    def authenticate(self):
        self.client.post(reverse('account:login'), data=dict(
            username='15201525181',
            password='test_password'
        ))

    def test_get_profile_info(self):
        """ 测试访问获取个人信息页面的数据
        """
        self.authenticate()
        response = self.client.get(reverse('profile:profile_info', args=(self.default_user.id, )))
        response_data = json.loads(response.content)
        profile = self.default_user.profile
        self.maxDiff = None
        self.assertEqual(
            response_data['user_profile'],
            {
                'nick_name': profile.nick_name,
                'age': profile.age,
                'avatar': profile.avatar.url,
                'gender': profile.get_gender_display(),
                'star_sign': profile.get_star_sign_display(),
                'district': profile.district,
                'job': profile.job,
                'signature': profile.signature,
                'status_num': 0,
                'fans_num': 0,
                'follow_num': 0,
            }
        )

    def tests_get_profile_with_avatar_club(self):
        """ 这个测试当目标用户具有签名俱乐部时返回数据是否正确
        """
        # First create a avatar_club
        club = Club.objects.create(name='test_club', host=self.default_user, logo='media/tests/test.png',
                                   description='test')
        profile = self.default_user.profile
        profile.avatar_club = club
        profile.save()
        # Visit the server
        self.authenticate()
        response = self.client.get(reverse('profile:profile_info', args=(self.default_user.id, )))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(
            response_data['user_profile']['avatar_club'],
            {
                'id': club.id,
                'club_logo': club.logo.url
            }
        )

    def test_get_profile_with_avatar_car(self):
        """ 这个测试当目标用户具有签名跑车时返回的数据是否正确
        """
        # First create a new car
        default_manufacturer = Manufacturer.objects.create(
            name=u'宝马',
            name_english=u'BMW',
        )
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        car = Sportscar.objects.create(
            name=u'Mini Cooper',
            name_english=u'Mini Cooper',
            price='300,000',
            seats=4,
            fuel_consumption=1,
            displacement=1.5,
            release_date=datetime.date(year=2000, month=1, day=1),
            logo=File(image),
            image=File(image),
            engine=u'4.5L 605马力V8',
            transmission=u'2门2座硬顶跑车',
            max_speed=u'325 km/h',
            zeroTo60='3s',
            manufacturer=default_manufacturer
        )
        self.default_user.profile.avatar_car = car
        self.default_user.profile.save()
        self.authenticate()
        response = self.client.get(reverse('profile:profile_info', args=(self.default_user.id, )))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(
            response_data['user_profile']['avatar_car'],
            {
                'car_id': car.id,
                'name': car.name,
                'logo': car.logo.url
            }
        )

    def test_get_profile_with_posted_status(self):
        default_manufacturer = Manufacturer.objects.create(
            name=u'宝马',
            name_english=u'BMW',
        )
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        car = Sportscar.objects.create(
            name=u'Mini Cooper',
            name_english=u'Mini Cooper',
            price='300,000',
            seats=4,
            fuel_consumption=1,
            displacement=1.5,
            release_date=datetime.date(year=2000, month=1, day=1),
            logo=File(image),
            image=File(image),
            engine=u'4.5L 605马力V8',
            transmission=u'2门2座硬顶跑车',
            max_speed=u'325 km/h',
            zeroTo60='3s',
            manufacturer=default_manufacturer
        )
        location = Location.objects.create(location=Point(120, 30), description='test', user=self.default_user)
        status_num = random.randint(1, 10)
        for _ in range(status_num):
            Status.objects.create(user=self.default_user, image='media/tests/test.png', content='status content',
                                  location=location, car=car)
        self.authenticate()
        response = self.client.get(reverse('profile:profile_info', args=(self.default_user.id, )))
        response_data = json.loads(response.content)
        self.assertEqual(response_data['user_profile']['status_num'], status_num)

    def test_get_profile_with_random_follows_and_fans(self):
        users = []
        for i in range(0, 10):
            users.append(get_user_model().objects.create(username=("username_%s" % i)))
        follow_num = random.randint(0, 9)
        for i in range(0, follow_num):
            UserFollow.objects.create(source_user=self.default_user, target_user=users[i])
        fans_num = random.randint(0, 9)
        for i in range(0, fans_num):
            UserFollow.objects.create(source_user=users[i], target_user=self.default_user)
        # Visit the server
        self.authenticate()
        response = self.client.get(reverse('profile:profile_info', args=(self.default_user.id, )))
        response_data = json.loads(response.content)
        self.assertEqual(response_data['user_profile']['fans_num'], fans_num)
        self.assertEqual(response_data['user_profile']['follow_num'], follow_num)

    def test_get_profile_for_other_user(self):
        user = get_user_model().objects.create(username='another_user')
        self.authenticate()
        response = self.client.get(reverse('profile:profile_info', args=(user.id, )))
        response_data = json.loads(response.content)
        self.assertFalse(response_data['user_profile']['followed'])
        UserFollow.objects.create(source_user=self.default_user, target_user=user)
        response = self.client.get(reverse('profile:profile_info', args=(user.id, )))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['user_profile']['followed'])

    def create_status(self, user=None, num=1):
        default_manufacturer = Manufacturer.objects.create(
            name=u'宝马',
            name_english=u'BMW',
        )
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        car = Sportscar.objects.create(
            name=u'Mini Cooper',
            name_english=u'Mini Cooper',
            price='300,000',
            seats=4,
            fuel_consumption=1,
            displacement=1.5,
            release_date=datetime.date(year=2000, month=1, day=1),
            logo=File(image),
            image=File(image),
            engine=u'4.5L 605马力V8',
            transmission=u'2门2座硬顶跑车',
            max_speed=u'325 km/h',
            zeroTo60='3s',
            manufacturer=default_manufacturer
        )
        location = Location.objects.create(location=Point(120, 30), description='test', user=self.default_user)
        if user is None:
            user = self.default_user
        status = []
        for _ in range(num):
            status.append(Status.objects.create(user=user, image='media/tests/test.png', content='status content',
                                                location=location, car=car))
        if num == 1:
            return status[0]
        else:
            return status

    def test_get_status_list_more(self):
        self.authenticate()
        status = self.create_status()
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('profile:status_list', args=(self.default_user.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data['data'], [{'id': status.id, 'image': status.image.url}])

    def test_get_status_list_latest(self):
        self.authenticate()
        status = self.create_status()
        request_time = timezone.now() - datetime.timedelta(seconds=60)
        response = self.client.get(reverse('profile:status_list', args=(self.default_user.id, )), data=dict(
            date_threshold=request_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            op_type='latest',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data['data'], [{'id': status.id, 'image': status.image.url}])

    def test_get_status_list_multiple_status(self):
        self.authenticate()
        status_num = random.randint(0, 20)
        self.create_status(num=status_num)
        request_time = timezone.now() + datetime.timedelta(seconds=60)
        response = self.client.get(reverse('profile:status_list', args=(self.default_user.id, )), data=dict(
            date_threshold = request_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            op_type='more',
            limit='10'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['data']), min(status_num, 10))

    def test_modify_test(self):
        #
        club = Club.objects.create(name='test_club', host=self.default_user, logo='media/tests/test.png',
                                   description='test')
        default_manufacturer = Manufacturer.objects.create(
            name=u'宝马',
            name_english=u'BMW',
        )
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        car = Sportscar.objects.create(
            name=u'Mini Cooper', name_english=u'Mini Cooper', price='300,000', seats=4, fuel_consumption=1,
            displacement=1.5, release_date=datetime.date(year=2000, month=1, day=1),
            logo=File(image), image=File(image), engine=u'4.5L 605马力V8',
            transmission=u'2门2座硬顶跑车', max_speed=u'325 km/h', zeroTo60='3s', manufacturer=default_manufacturer
        )
        SportCarOwnership.objects.create(user=self.default_user, car=car, signature='', identified=True,
                                         identified_at=timezone.now())
        #
        self.authenticate()
        new_avatar = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test2.png'))
        response = self.client.post(reverse('profile:modify'), data=dict(
            nick_name='new_name',
            avatar_club=club.id,
            avatar_car=car.id,
            signature='new signature',
            job='new job',
            district='new district',
            avatar=new_avatar
        ))
        new_avatar.close()
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))
        profile = UserProfile.objects.get(user=self.default_user)
        self.assertEqual(profile.avatar_club.id, club.id)
        self.assertEqual(profile.nick_name, 'new_name')
        self.assertEqual(profile.avatar_car.id, car.id)
        self.assertEqual(profile.signature, 'new signature')
        self.assertNotEqual(profile.avatar.url, '/media/test/tests.png')
        self.assertEqual(profile.job, 'new job')
        self.assertEqual(profile.district, 'new district')

    def test_modify_single_property(self):
        """ 这个测试测试单独修改某一个属性是否成功
        """
        #
        self.authenticate()
        response = self.client.post(reverse('profile:modify'), data=dict(
            nick_name='new_name'
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))
        profile = UserProfile.objects.get(user=self.default_user)
        self.assertEqual(profile.nick_name, 'new_name')

    def test_modify_non_exist_club(self):
        self.authenticate()
        response = self.client.post(reverse('profile:modify'), data=dict(
            avatar_club=1000,
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='2002',
                                             message='Club not found or you have not joined the club yet.'))

    def test_modify_club_not_joined_yet(self):
        self.authenticate()
        new_user = get_user_model().objects.create(username='another_user')
        club = Club.objects.create(name='test_club', host=new_user, logo='media/tests/test.png',
                                   description='test')
        response = self.client.post(reverse('profile:modify'), data=dict(
            avatar_club=club.id,
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=False, code='2002',
                                             message='Club not found or you have not joined the club yet.'))

    def test_modify_non_exist_car(self):
        self.authenticate()
        response = self.client.post(reverse('profile:modify'), data=dict(
            avatar_car=1000,
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         dict(success=False, code='2003', message='Car not found or you do not own this car'))

    def test_modify_car_not_owned_by_the_user(self):
        new_user = get_user_model().objects.create(username='another_user')
        default_manufacturer = Manufacturer.objects.create(
            name=u'宝马',
            name_english=u'BMW',
        )
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        car = Sportscar.objects.create(
            name=u'Mini Cooper', name_english=u'Mini Cooper', price='300,000', seats=4, fuel_consumption=1,
            displacement=1.5, release_date=datetime.date(year=2000, month=1, day=1),
            logo=File(image), image=File(image), engine=u'4.5L 605马力V8',
            transmission=u'2门2座硬顶跑车', max_speed=u'325 km/h', zeroTo60='3s', manufacturer=default_manufacturer
        )
        self.authenticate()
        response = self.client.post(reverse('profile:modify'), data=dict(
            avatar_car=car.id,
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         dict(success=False, code='2003', message='Car not found or you do not own this car'))
        SportCarOwnership.objects.create(user=new_user, car=car, signature='', identified=False,
                                         identified_at=timezone.now())
        response = self.client.post(reverse('profile:modify'), data=dict(
            avatar_car=car.id,
        ))
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         dict(success=False, code='2003', message='Car not found or you do not own this car'))

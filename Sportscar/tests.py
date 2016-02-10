# coding=utf-8
import os
import json
import datetime

from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.files import File

from .models import Sportscar, Manufacturer, SportCarOwnership
# Create your tests here.


class CarViewTest(TestCase):

    def setUp(self):
        self.default_manufacturer = Manufacturer.objects.create(
            name=u'宝马',
            name_english=u'BMW',
        )
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        self.car1 = Sportscar.objects.create(
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
            transmission=u'7缸双离合',
            max_speed=u'325 km/h',
            zeroTo60='3s',
            manufacturer=self.default_manufacturer,
            body=u"2门2坐硬顶跑车"
        )
        image.close()
        self.user = get_user_model().objects.create(username='15201525181')
        self.user.set_password('huang9040601')
        self.user.save()

        self.client = Client()

    def default_authenticate(self):
        self.client.post(reverse('account:login'), data=dict(username='15201525181', password='huang9040601'))

    def test_type_list(self):
        response = self.client.get(reverse('cars:type_list'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(
            success=True,
            cars=[dict(
                brand_name=u'宝马',
                detail_list=[dict(name=u'Mini Cooper', id=self.car1.id)]
            )]
        ))

    def test_get_car_information(self):
        self.default_authenticate()
        response = self.client.get(reverse('cars:car_detail', kwargs={'car_id': self.car1.id}))
        response_data = json.loads(response.content)
        self.maxDiff = None
        self.assertEqual(response_data, dict(
            success=True,
            data=dict(
                logo_url=self.car1.logo.url,
                image_url=self.car1.image.url,
                engine=u'4.5L 605马力V8',
                transmission=u'7缸双离合',
                max_speed=u'325 km/h',
                zeroTo60=u'3s',
                manufacturer_name=u'宝马',
                car_name=u'Mini Cooper',
                body=u'2门2坐硬顶跑车',
                price=u'300,000',
                car_id=self.car1.id,
                owned=False,
            )
        ))

    def test_car_follow(self):
        self.default_authenticate()
        response = self.client.post(reverse('cars:car_follow', args=(self.car1.id, )),
                                    data=dict(signature='test'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(success=True))

    def test_car_follow_with_invalid_car_id(self):
        self.default_authenticate()
        response = self.client.post(reverse('cars:car_follow', args=(100, )),
                                    data=dict(signature='test'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(
            success=False,
            message='Sport car not found.',
            code='1004'
        ))

    def test_car_login_without_login(self):
        response = self.client.post(reverse('cars:car_follow', args=(100, )),
                                    data=dict(signature='test'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data, dict(
            success=False,
            message='You need to login first',
            code='1402'))

    def test_car_auth(self):
        SportCarOwnership.objects.create(user=self.user, car=self.car1, signature='test')
        self.default_authenticate()
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        response = self.client.post(reverse('cars:auth'), data=dict(
            car_id=self.car1.id,
            image1=image, image2=image, image3=image, id_card=image,
            license='test'
        ))
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_car_auth_no_permission(self):
        self.default_authenticate()
        image = open(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, 'tests', 'test.png'))
        response = self.client.post(reverse('cars:auth'), data=dict(
            car_id=self.car1.id,
            image1=image, image2=image, image3=image, id_card=image,
            license='test'
        ))
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def test_car_query(self):
        self.default_authenticate()
        response = self.client.get(reverse('cars:query'), data=dict(
            manufacturer=self.default_manufacturer.name,
            car_name=self.car1.name
        ))
        self.assertEqual(response.status_code, 302)
    # TODO: 后续在这里要加上允许的通过的申请的功能的测试


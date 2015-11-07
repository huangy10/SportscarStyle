# coding=utf-8
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators import http as http_decorators
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import Manufacturer, Sportscar, SportCarOwnership, SportCarIdentificationRequestRecord
from custom.utils import post_data_loader, login_first
# Create your views here.


@cache_page(60 * 60 * 24)           # Since the result of this view seldom changes, cache it for a entire day
@http_decorators.require_GET
def cars_type_list(request):
    """ Request for the information for the available sport cars.
    """
    all_manufacturers = Manufacturer.objects.all()

    def type_parser(manufacturer):
        result = {'brand_name': manufacturer.name}
        details = Sportscar.objects.filter(manufacturer=manufacturer).values('name', 'id')
        result['detail_list'] = list(details)
        return result

    data = map(type_parser, all_manufacturers)
    return JsonResponse(dict(
        success=True,
        cars=data,
    ))


@http_decorators.require_GET
def cars_detail(request, car_id):
    """ Query for the information about a specific sport car with the car id
     :param car_id id of the car

     the default response data includes:
        - manufacturer_name:
        - car_name:
        - engine:
        - transmission:
        - max_speed:
        - zeroTo60:
        - logo_url:
        - image_url

    """
    # you can specify the response data type by the `type` GET param
    query_type = request.GET.get('type', 'default')
    result = dict(success=True)
    if query_type == 'default':
        try:
            car = Sportscar.objects.get(id=car_id)
            result['data'] = dict(
                manufacturer_name=car.manufacturer.name,
                car_name=car.name,
                engine=car.engine,
                transmission=car.transmission,
                max_speed=car.max_speed,
                zeroTo60=car.zeroTo60,
                logo_url=car.logo.url,
                image_url=car.image.url
            )
        except ObjectDoesNotExist:
            result['success'] = False
            result['code'] = 1004
            result['message'] = 'Sport car not found.'
    return JsonResponse(result)


@http_decorators.require_POST
@login_first
@post_data_loader()
def car_follow(request, data, car_id):
    """ Follow a car
     POST data:
        - signature:
    """
    try:
        car = Sportscar.objects.get(pk=car_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(
            success=False,
            message='Sport car not found.',
            code='1004'
        ))
    SportCarOwnership.objects.get_or_create(user=request.user,
                                            car=car,
                                            signature=data['signature'])
    return JsonResponse(dict(success=True))


@http_decorators.require_POST
@login_first
@post_data_loader()
def car_auth(request, data):
    """ 跑车认证接口, 车主通过这个车主认证跑车确实为自己所有
     上传的参数包括:
        -------
         |- car_id
         |- image1:
         |- image2:
         |- image3:
         |- id_card:
         |- license:
    """
    # 首先查询申请是否已经存在
    try:
        record = SportCarIdentificationRequestRecord.objects.get(
            ownership__car_id=data['car_id'], ownership__user=request.user)
        if record.approved:
            return JsonResponse(dict(success=False, message=u'该车主的该车辆已经被认证了', code='2400'))
        elif SportCarOwnership.objects.filter(car_id=data['car_id'], user=request.user).exists():
            record.image = [request.FILES['image1'], request.FILES['image2'], request.FILES['image3']]
            record.id_card = request.FILES['id_card']
            record.license_num = data['license']
            record.save()
            return JsonResponse(dict(success=True))
        else:
            return JsonResponse(dict(success=False, message=u'没有权限', code='2401'))
    except ObjectDoesNotExist:
        try:
            owner_ship = SportCarOwnership.objects.get(car_id=data['car_id'], user=request.user)
            SportCarIdentificationRequestRecord.objects.create(
                ownership=owner_ship,
                images=[request.FILES['image1'], request.FILES['image2'], request.FILES['image3']],
                id_card=request.FILES['id_card'],
                license_num=data['license']
            )
            return JsonResponse(dict(success=True))
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message=u'没有权限', code='2401'))






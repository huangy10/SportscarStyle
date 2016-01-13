# coding=utf-8
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators import http as http_decorators
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
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
        - car_id:
        - price
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
                image_url=car.image.url,
                body=car.body,
                price=car.price,
                car_id=car.id
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

@http_decorators.require_GET
@login_first
def car_authed_list(request, user_id):
    """ 获取制定user_id的用户所拥有的车辆
     :param user_id

     返回的数据为车辆组成的数组,其中每个元素包含的信息是
    """
    ownership =SportCarOwnership.objects.filter(user_id=user_id)
    return JsonResponse(success=True, data=map(lambda x: x.dict_description(), ownership))


@http_decorators.require_GET
@login_first
def car_query_by_name(request):
    manufacturer = request.GET['manufacturer']
    car_name = request.GET['car_name']
    print request
    print manufacturer, car_name
    try:
        car = Sportscar.objects.get(name=car_name, manufacturer__name=manufacturer)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False))

    return HttpResponseRedirect(reverse("cars:car_detail", args=(car.id, )))




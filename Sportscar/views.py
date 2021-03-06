# coding=utf-8
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators import http as http_decorators
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q

from .models import Manufacturer, Sportscar, SportCarOwnership, SportCarIdentificationRequestRecord
from Status.models import Status
from custom.utils import post_data_loader, login_first
# Create your views here.


@http_decorators.require_GET
def cars_type_list(request):
    """ Request for the information for the available sport cars.
    """
    scope = request.GET["scope"]
    if scope == "manufacturer":
        filter_string = request.GET.get("filter", "")
        if filter_string == "":
            filter_q = Q()
        else:
            filter_q = Q(name__icontains=filter_string)
        indexes = u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = dict()
        for index in indexes:
            temp = Manufacturer.objects.filter(filter_q, index__iexact=index).values_list("name", flat=True)
            if temp.count() > 0:
                result[index] = list(temp)
        return JsonResponse(dict(success=True, data=result))
    if scope == "car_name":
        manufacturer_name = request.GET["manufacturer"]
        result = Sportscar.objects.filter(manufacturer__name=manufacturer_name).values_list("name", flat=True)
        return JsonResponse(dict(success=True, data=list(result)))
    if scope == "sub_name":
        manufacturer_name = request.GET["manufacturer"]
        name = request.GET["car_name"]
        result = Sportscar.objects.filter(manufacturer__name=manufacturer_name, name=name).values_list(
            "subname", flat=True
        )
        print result
        return JsonResponse(dict(success=True, data=list(result)))


@http_decorators.require_GET
@login_first
def cars_detail(request, car_id):
    """ 根据给定的跑车的id,获取其详细信息,伴随返回的还有和此跑车相关的(最多)三条状态
     :param car_id id of the car

     the default response data includes:
        | manufacturer_name:
        | car_name:
        | engine:
        | transmission:
        | max_speed:
        | zeroTo60:
        | logo_url:
        | image_url
        | car_id:
        | price
        |-- related_status
            | id
            | image
        | identified: 是否是当前用户认证了的车辆
        | signature: 跑车签名
        | owned: 是否由当前用户所拥有,若为false,则上面的identified和signature属性将不会存在
    """
    # you can specify the response data type by the `type` GET param
    query_type = request.GET.get('type', 'default')
    result = dict(success=True)
    if query_type == 'default':
        try:
            data = dict()
            try:
                ownership = SportCarOwnership.objects.select_related("car").get(user=request.user, car_id=car_id)
                car = ownership.car
                data["identified"] = ownership.identified
                data["signature"] = ownership.signature
                data["owned"] = True
                related_status = Status.objects.filter(user=request.user, car_id=car_id).order_by("-created_at")[0:4]
                data["related_status"] = map(lambda x: {"id": x.id, "image": x.image1.url}, related_status)

            except ObjectDoesNotExist:
                car = Sportscar.objects.get(id=car_id)
                data["owned"] = False

            # data.update(dict(
            #     manufacturer_name=car.manufacturer.name,
            #     car_name=car.name,
            #     engine=car.engine,
            #     transmission=car.transmission,
            #     max_speed=car.max_speed,
            #     zeroTo60=car.zeroTo60,
            #     logo_url=car.manufacturer.logo.url,
            #     image_url=car.image.url,
            #     body=car.body,
            #     price=car.price,
            #     carID=car.id,
            # ))
            data.update(car.dict_description())
            result["data"] = data

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
    if SportCarOwnership.objects.filter(
        user=request.user, identified=False
    ).count() >= 1:
        return JsonResponse(dict(success=False, message="No permission"))
    own, created = SportCarOwnership.objects.get_or_create(
        user=request.user,
        car=car,
        signature=data['signature']
    )
    return JsonResponse(dict(success=True, data=own.dict_description()))


@http_decorators.require_POST
@login_first
def car_delete(request, car_id):
    try:
        follow = SportCarOwnership.objects.get(user=request.user, car__id=car_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message=u"Car Not Found"))
    follow.delete()
    return JsonResponse(dict(success=True))


@http_decorators.require_POST
@login_first
def car_update_signature(request, car_id):
    try:
        follow = SportCarOwnership.objects\
            .get(user=request.user, car__id=car_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message=u"Car Not Found"))
    follow.signature = request.POST['signature']
    follow.save()
    return JsonResponse(dict(success=True))


@http_decorators.require_POST
@login_first
@post_data_loader()
def car_auth(request, data):
    """ 跑车认证接口, 车主通过这个车主认证跑车确实为自己所有
     上传的参数包括:
        -------
         |- car_id
         |- drive_license:
         |- photo:
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
            record.drive_license = request.FILES["drive_license"]
            if "photo" in request.FILES:
                record.photo = request.FILES["photo"]
            if "id_card" in request.FILES:
                record.id_card = request.FILES['id_card']
            if "car_license" in request.FILES:
                record.photo = request.FILES["car_license"]
            if "drive_license" in request.FILES:
                record.drive_license = request.FILES["drive_license"]
            record.license_num = data['license']
            record.save()
            return JsonResponse(dict(success=True))
        else:
            return JsonResponse(dict(success=False, message=u'没有权限', code='2401'))
    except ObjectDoesNotExist:
        try:
            owner_ship = SportCarOwnership.objects.get(car_id=data['car_id'], user=request.user)
            reserved_data = dict()
            if "photo" in request.FILES:
                reserved_data['photo'] = request.FILES['photo']
            if "id_card" in request.FILES:
                reserved_data['id_card'] = request.FILES['id_card']
            if "car_license" in request.FILES:
                reserved_data['photo'] = request.FILES['car_license']
            record = SportCarIdentificationRequestRecord.objects.create(
                ownership=owner_ship,
                drive_license=request.FILES["drive_license"],
                # photo=request.FILES["photo"],
                # id_card=request.FILES['id_card'],
                license_num=data['license'],
                **reserved_data
            )
            if "car_license" in request.FILES:
                record.photo = request.FILES["car_license"]
                record.save()

            return JsonResponse(dict(success=True))
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, message=u'没有权限', code='2401'))


@http_decorators.require_GET
@login_first
def car_query_by_name(request):
    manufacturer = request.GET['manufacturer']
    car_name = request.GET['car_name']
    sub_name = request.GET.get('sub_name', "")

    try:
        car = Sportscar.objects.get(name=car_name, manufacturer__name=manufacturer, subname=sub_name)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False))

    return HttpResponseRedirect(reverse("cars:car_detail", args=(car.id, )))



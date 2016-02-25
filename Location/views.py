# coding=utf-8
import datetime

from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Sum, Q
from django.db import models
from django.utils import timezone

from .models import Location, UserTracking
from custom.utils import login_first, post_data_loader
# Create your views here.

filter_types = [
    'near_popular',
    'my_follows',
    'my_fans',
    'my_friends',
    'club_only'
]


@require_POST
@login_first
@post_data_loader()
def radar_cars(request, data):
    """ 跑车雷达:获取车主的位置数据, 筛选条件的格式如下:
     - filter:  筛选器编号
     - filter_param: 筛选需要提供的额外参数

     - loc
      |- lat
      |- lon
    """
    # 首先更新用户的位置
    lat = float(data["loc"]["lat"])
    lon = float(data["loc"]["lon"])
    tracking = request.user.location
    loc = tracking.location
    loc.location = Point(lon, lat)
    loc.save()
    # 自动更新了时间
    tracking.save()

    if not tracking.location_available:
        tracking.location_available = True
        tracking.save()

    filter_type = data["filter"]
    if filter_type == "distance":
        distance = float(data["filter_param"])

        # TODO: 添加其他的筛选条件

        results = get_user_model().objects.select_related("profile", "location")\
            .annotate(authed_cars_num=Case(
                        When(
                                ownership__identified=True,
                                then=1),
                        default=0, output_field=models.IntegerField()))\
            .filter(~Q(id=request.user.id), authed_cars_num__gt=0,
                    location__location__location__distance_lte=(loc.location, D(km=distance)),
                    location__location_available=True,
                    location__updated_at__gt=(timezone.now() - datetime.timedelta(seconds=300)))\
            .distinct()

        def result_generator(user):
            result = user.profile.complete_dict_description()
            result["loc"] = user.location.location.dict_description()
            return result

        return JsonResponse(dict(success=True, result=map(result_generator, results)))


@require_POST
@login_first
@post_data_loader()
def radar_user_location_udpate(request, data):
    """ 更新用户的当前位置
    """
    lat = float(data["lat"])
    lon = float(data["lon"])
    tracking = request.user.location
    loc = tracking.location
    loc.location = Point(lon, lat)
    loc.save()  # 自动更新了时间
    if not tracking.location_available:
        tracking.location_available = True
        tracking.save()

    return JsonResponse(dict(success=True))

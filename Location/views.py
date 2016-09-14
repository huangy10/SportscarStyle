# coding=utf-8
import datetime

from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Count, Case, When, Sum, Q
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Location, UserTracking
from custom.utils import login_first, post_data_loader
from User.models import User


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

      Updated by Woody Huang, 2016.07.10
        Enable "blacklist" functionality
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
    # load the scan center
    lat = float(data["scan_center"]["lat"])
    lon = float(data["scan_center"]["lon"])
    filter_type = data["filter"]
    try:
        distance = float(data["scan_distance"])
    except KeyError:
        # 向下兼容
        distance = float(data["filter_param"])

    results = User.objects.select_related("location") \
        .annotate(authed_cars_num=Case(When(ownership__identified=True, then=1),
                                       default=0, output_field=models.IntegerField())) \
        .filter(~Q(id=request.user.id) & ~Q(blacklist_by=request.user),
                authed_cars_num__gte=0,
                location__location__location__distance_lte=(Point(x=lon, y=lat), D(km=distance)),
                location__location_available=True,
                location__updated_at__gt=(timezone.now() - datetime.timedelta(days=3))) \
        .distinct()

    def result_generator(user):
        result = user.dict_description(detail=True)
        result["loc"] = user.location.location.dict_description()
        return result

    if filter_type == "distance":
        return JsonResponse(dict(success=True, result=map(result_generator, results)))
    elif filter_type == "follows":
        results = results.filter(fans=request.user)
        return JsonResponse(dict(success=True, result=map(result_generator, results)))
    elif filter_type == "fans":
        results = results.filter(follows=request.user)
        return JsonResponse(dict(success=True, result=map(result_generator, results)))
    elif filter_type == "friends":
        results = results.filter(follows=request.user, fans=request.user)
        return JsonResponse(dict(success=True, result=map(result_generator, results)))
    elif filter_type == "club":
        club_id = data["filter_param"]["club_id"]
        results = results.filter(club_joined=club_id)
        return JsonResponse(dict(success=True, result=map(result_generator, results)))
    else:
        return JsonResponse(dict(success=False))


@require_POST
@login_first
@post_data_loader()
def radar_user_location_udpate(request, data):
    """ 更新用户的当前位置
    """
    print data
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


@require_GET
@login_first
def track_user(request, user_id):
    """ Fetch the latest location of the given user
    """
    try:
        target_user = User.objects.select_related("location").get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message="user not found"))
    time_delta = timezone.now() - target_user.location.updated_at
    # if time_delta.seconds > 300:
    #     return JsonResponse(dict(success=True, location=None))
    # # TODO: Check the permission of the current user
    return JsonResponse(dict(success=True, location=target_user.location.location.dict_description()))

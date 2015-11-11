# coding=utf-8
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.contrib.gis.geos import Point

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
    # 首先进行当前的用户的位置更新
    loc = Location.objects.create(location=Point(data['loc']['lon'], data['loc']['lat']))
    UserTracking.objects.create(location=loc, user=request.user)
    #
    filter_type = data['filter']
    if filter_type not in filter_types:
        return JsonResponse(dict(success=False, code='5300', message='Filter not defined.'))
    if filter_type == 'near_popular':
        range = require_GET['filter_param']

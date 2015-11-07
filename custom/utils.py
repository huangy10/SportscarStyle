# coding=utf-8

import uuid
import json
import pytz
from datetime import datetime

from django.http import JsonResponse
from django.utils import timezone
from django.test import Client

def path_creator(method):
    """这个装饰器用来构造作为Django自带的ImageField的upload_to参数的函数
     :param method 被装饰的函数应当返回一个目录名称
    """
    def wrapper(instance, filename, *args, **kwargs):
        root_path = method()
        current = datetime.datetime.now()
        ext = filename.split('.')[-1]
        random_file_name = str(uuid.uuid4()).replace('-', '')
        new_file_name = "{0}/{1}/{2}/{3}/{4}.{5}".format(
            root_path,
            current.year,
            current.month,
            current.day,
            random_file_name,
            ext
        )
        return new_file_name

    return wrapper


def post_data_loader(force_json=False, json_fields=None):
    """这个装饰器用来解析出上传数据，首先尝试解析json，如果失败，则认为post数据在request的字典中

     注意使用这个装饰器的view在request之后的形参要用作数据输入使用

     :param force_json      只接受json数据包
     :param json_field      request.POST的某系字段需以json方式解析，解析后的数据会放置在request.POST.json_data中
    """
    if not json_fields:
        json_fields = []

    def wrapper(method):
        def _wrapper(request, **kwargs):
            if request.method != 'POST':
                return method(request, data=None, **kwargs)
            try:
                data = json.loads(request.body)
            except ValueError:
                if force_json:
                    return JsonResponse(dict(success=False, code='0000', message='This views need json request.'))
                data = request.POST

                if json_fields is not None and len(json_fields) > 0:
                    if len(json_fields) == 1:
                        json_data = json.loads(request.POST.get(json_fields[0], "{}"))
                    else:
                        json_data = {}
                        for field_name in json_fields:
                            json_data[field_name] = json.loads(request.POST.get(field_name, "{}"))
                    # setattr(data, 'json_data', json_data)
                    data['json_data'] = json_data
            return method(request, data, **kwargs)
        return _wrapper
    return wrapper


def login_first(method):
    """ 这个装饰器和django自带的不同，如果发现当前用户没有登陆，会返回一个Json告知
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse(dict(success=False, message='You need to login first',
                                code='1402'))
        else:
            return method(request, *args, **kwargs)
    return wrapper


def page_separator_loader(method):
    """ 这个装饰器从GET中载入分页参数，如果发现参数缺失，会返回错误
     - GET data:
        - date_threshold:
        - op_type:
        - limit:
    """
    def wrapper(request, *args, **kwargs):
        error_dict = dict(
            success=False,
            code='3300',
            message='Param lost.'
        )
        if 'date_threshold' in request.GET and 'op_type' in request.GET and 'limit' in request.GET:
            try:
                date_threshold = datetime.strptime(request.GET['date_threshold'], '%Y-%m-%d %H:%M:%S %Z')
                date_threshold = timezone.make_aware(date_threshold)
                limit = int(request.GET['limit'])
                limit = min(limit, 1000)
                op_type = request.GET.get('op_type')
                if op_type not in ['latest', 'more']:
                    return JsonResponse(dict(
                        success=False, code='3400', message='invalid op_type'
                    ))
            except ValueError:
                return JsonResponse(error_dict)
            return method(request, date_threshold=date_threshold, op_type=request.GET['op_type'], limit=limit,
                          *args, **kwargs)
        else:
            return JsonResponse(error_dict)
    return wrapper

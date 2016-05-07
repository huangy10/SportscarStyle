# coding=utf-8
import logging

from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators import http as http_decorators
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from django.utils import timezone

from Profile.utils import send_sms, create_random_code, star_sign_from_date
from .models import User, AuthenticationCode, CorporationAuthenticationRequest, UserRelation
from .forms import RegistrationForm, PasswordResetForm, CorporationUserApplicationCreateForm
from .utils import JWTUtil
from Club.models import Club, ClubJoining
from Sportscar.models import Sportscar, SportCarOwnership
from Status.models import Status, StatusLikeThrough
from custom.utils import *
from Notification.signal import send_notification
from Notification.models import RegisteredDevices

logger = logging.getLogger(__name__)


@http_decorators.require_POST
@post_data_loader()
def account_login(request, data):
    """
    User login through this api.
    :param request:
    :param data:
    :return:
    """
    username = data.get('username')
    password = data.get('password')
    token = data.get('device_token', None)
    device_id = data.get('device_id', None)
    if token is None and device_id is None:
        return JsonResponse(dict(success=False, message="Identifier for device required"))
    user = auth.authenticate(username=username,
                             password=password)
    if user is None:
        # fail to authenticate
        if not User.objects.filter(username=username).exists():
            return JsonResponse(dict(success=False, message="Invalid username", code=1000))
        else:
            return JsonResponse(dict(success=False, message="Password Incorrect", code=1001))
    else:
        # auth.login(request, user)
        if token is not None:
            RegisteredDevices.objects.filter(user=user).update(is_active=False)
            device, _ = RegisteredDevices.objects.get_or_create(
                user=user,
                token=token,
                device_type="ios",
                device_id=device_id or token
            )
            if not device.is_active:
                device.is_active = True
                device.save()
        jwt_token = JWTUtil.jwt_encode(user.id, device_id or token)
        result = user.dict_description()
        # include the jwt token
        result.update(jwt_token=jwt_token)
        return JsonResponse(dict(success=True, data=result))


@http_decorators.require_POST
@login_first
@post_data_loader()
def account_logout(request, data):
    """
    logout
    :param request:
    :param data:
    :return:
    """
    token = data.get("device_token", None)
    if token is not None:
        RegisteredDevices.objects.filter(user=request.user, token=token)\
            .update(is_active=False)
    auth.logout(request)
    return JsonResponse(dict(success=True))


@http_decorators.require_POST
@post_data_loader()
def account_register(request, data):
    """
    Create new user through this interface
     This method only accept post request
    :param request:
    :param data:
    :return:
    """
    print data
    token = data.get('device_token', None)
    device_id = data.get('device_id', None)
    if token is None and device_id is None:
        return JsonResponse(dict(success=False, message="Identifier for device required"))
    form = RegistrationForm(data)
    if form.is_valid():
        user = form.save()
        user = auth.authenticate(
            username=user.username,
            password=data.get("password"))
        if user is None:
            logger.error("fatal error!")
        # auth.login(request, user)
        if token is not None:
            device, _ = RegisteredDevices.objects.get_or_create(
                user=user,
                token=token,
                device_type="ios",
                device_id=device_id or token
            )
            if not device.is_active:
                device.is_active = True
                device.save()
        jwt_token = JWTUtil.jwt_encode(user.id, device_id or token)
        result = user.dict_description()
        # include the jwt token
        result.update(jwt_token=jwt_token)
        return JsonResponse(dict(success=True, data=result))
    else:
        response_dict = dict(success=False, code='1002')
        response_dict.update(form.errors)
        print response_dict
        return JsonResponse(response_dict)


@http_decorators.require_POST
@post_data_loader()
def account_send_code(request, data):
    """ Request for authentication code
     POST params:
        - phone_num: phone number
    """
    phone_num = data.get('phone_num', None)
    print phone_num
    if AuthenticationCode.objects.already_sent(phone=phone_num):
        return JsonResponse(dict(success=False, message='request too frequent',
                                 code='1400'))
    else:
        code = create_random_code()
        if send_sms(code, phone_num):
            AuthenticationCode.objects.create(phone_num=phone_num, code=code)
            return JsonResponse(dict(success=True))
        else:
            return JsonResponse(dict(success=False, message='error occurs in the SMS backend',
                                     code='1401'))


@http_decorators.require_POST
@post_data_loader()
def account_reset_password(request, data):
    """
    Reset password
    :param request:
    :param data:
    :return:
    """
    form = PasswordResetForm(data)
    token = data.get('device_token', None)
    device_id = data.get('device_id', None)
    if token is None and device_id is None:
        return JsonResponse(dict(success=False, message="Identifier for device required"))
    if form.is_valid():
        form.save()
        user = auth.authenticate(username=data["username"], password=data["password"])
        # auth.login(request, new_user)
        if token is not None:
            device, _ = RegisteredDevices.objects.get_or_create(
                user=user,
                token=token,
                device_type="ios",
                device_id=device_id or token
            )
            if not device.is_active:
                device.is_active = True
                device.save()
        jwt_token = JWTUtil.jwt_encode(user.id, device_id or token)
        result = user.dict_description()
        # include the jwt token
        result.update(jwt_token=jwt_token)
        return JsonResponse(dict(success=True, data=result))
    else:
        response_dict = dict(success=False)
        response_dict.update(form.errors)
        return JsonResponse(response_dict)


@http_decorators.require_POST
@login_first
@post_data_loader()
def account_set_profile(request, data):
    """
     set account after register
    :param request:
    :param data:
        POST params:
        - nick_name:
        - gender:m or f
        - birth_date: birth date
        - avatar:
    :return:
    """
    user = request.user
    user.nick_name = data['nick_name']
    user.gender = data['gender']
    user.birth_date = datetime.strptime(data['birth_date'], "%Y-%m-%d")
    user.star_sign = star_sign_from_date(user.birth_date)
    user.avatar = request.FILES['avatar']
    user.save()
    return JsonResponse(dict(success=True))

#######################################################################################################################
#
# 以下是个人中心部分使用的API
#
#######################################################################################################################


@http_decorators.require_GET
@login_first
def profile_info(request, user_id):
    """
    Get the detail information about the user
    :param request:
    :param user_id:  the id of the user
    :return:
    """
    try:
        user = User.objects.select_related('avatar_car', 'avatar_club')\
            .get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code=2000, message="User not found"))

    return JsonResponse(dict(success=True, data=user.dict_description(detail=True, host=request.user)))


@http_decorators.require_POST
@login_first
def profile_corporation_user_authenticate(request):
    if request.user.corporation_identified:
        return JsonResponse(dict(success=False, message="already authed"))
    try:
        CorporationAuthenticationRequest.objects.get(user=request.user, revoked=False)
        return JsonResponse(dict(success=False, message='authentication ongoing'))
    except ObjectDoesNotExist:
        pass
    form = CorporationUserApplicationCreateForm({'user': request.user.id}, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse(dict(success=True))
    else:
        print form.errors
        return JsonResponse(dict(success=False))


@http_decorators.require_GET
@login_first
@page_separator_loader
def profile_status_list(request, date_threshold, op_type, limit, user_id):
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)
    car_query_id = request.GET.get('filter_car', None)
    if car_query_id is not None:
        car_query = Q(car_id=car_query_id)
    else:
        car_query = Q()
    data = Status.objects.filter(date_filter & car_query, user__id=user_id, deleted=False)\
        .order_by('-created_at')[0:limit]

    data = map(lambda x: x.dict_description(), data)
    # TODO: 这里还需要返回status创建的时间
    return JsonResponse(dict(success=True, data=data))


@http_decorators.require_POST
@login_first
@post_data_loader()
def profile_modify(request, data):
    """
     Modify the profile settings. You can modify any number of properties
    :param request:
    :param data:
    :return:
    """
    print "modify"
    modiable_properties = ['nick_name', 'avatar', 'avatar_club', 'avatar_car', 'signature',
        'job', 'district']
    for key in data:
        if key not in modiable_properties:
            return JsonResponse(dict(success=False, code='2001', message='Invalid property name.'))

    user = request.user
    if 'avatar' in request.FILES:
        user.avatar = request.FILES['avatar']

    user.nick_name = data.get('nick_name', user.nick_name)
    user.signature = data.get('signature', user.signature)
    user.job = data.get('job', user.job)
    user.district = data.get('district', user.district)

    if 'avatar_club' in data:
        try:
            join = ClubJoining.objects.get(user=request.user, club_id=data['avatar_club'])
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code='2002',
                                     message='Club not found or you have not joined the club yet.'))
        user.avatar_club = join

    if 'avatar_car' in data:
        try:
            ownership = SportCarOwnership.objects.get(user=request.user, car_id=data['avatar_car'])
        except ObjectDoesNotExist:
            return JsonResponse(dict(success=False, code='2003', message='Car not found or you do not own this car'))
        user.avatar_car = ownership

    user.save()
    return JsonResponse(dict(success=True, data=user.dict_description(detail=True)))


@http_decorators.require_GET
@login_first
@page_separator_loader
def profile_fans_list(request, date_threshold, op_type, limit, user_id):
    """
     Query for the fans of a user
    :param request:
    :param date_threshold:
    :param op_type:
    :param limit:
    :param user_id:
    :return:
    """
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=True, message='User not found', code='2000'))
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    filter_str = request.GET.get("filter", "")
    if filter_str != "":
        filter_elements = filter_str.split(" ")
        filter_q = Q()
        for filter_element in filter_elements:
            filter_q = filter_q | Q(target_user__profile__nick_name__icontains=filter_element)
    else:
        filter_q = Q()

    fans = UserRelation.objects.select_related('source_user')\
        .filter(date_filter & filter_q, target_user=user)[0:limit]

    return JsonResponse(dict(success=True, data=map(lambda x: x.dict_description(), fans)))


@http_decorators.require_GET
@login_first
@page_separator_loader
def profile_follow_list(request, date_threshold, op_type, limit, user_id):
    """
     Query for the follows of a user
    :param request:
    :param date_threshold:
    :param op_type:
    :param limit:
    :param user_id:
    :return:
    """
    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=True, message='User not found', code='2000'))
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    filter_str = request.GET.get("filter", "")
    if filter_str != "":
        filter_elements = filter_str.split(" ")
        filter_q = Q()
        for filter_element in filter_elements:
            filter_q = filter_q | Q(target_user__profile__nick_name__icontains=filter_element)
    else:
        filter_q = Q()

    follows = UserRelation.objects.select_related('target_user') \
        .filter(date_filter & filter_q, source_user=user)[0:limit]

    return JsonResponse(dict(success=True, data=map(lambda x: x.dict_description(), follows)))


@http_decorators.require_POST
@post_data_loader()
def profile_operation(request, data, user_id):
    """
     Operations about account, For now, only follow/unfollow are implemented.
    :param request:
    :param data:
    :param user_id:
    :return:
    """
    op_type = data.get('op_type')
    if op_type not in ['follow']:
        return JsonResponse(dict(success=False, code='2300', message='No valid operation type param found.'))
    if int(user_id) == request.user.id:
        return JsonResponse(dict(success=False, code='2301', message='Invalid operation'))
    try:
        target_user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message='User not found', code='2000'))

    if op_type == 'follow':
        obj, created = UserRelation.objects.get_or_create(source_user=request.user, target_user=target_user)
        if not created:
            obj.delete()
        else:
            send_notification.send(sender=User,
                                   target=target_user,
                                   message_type="relation_follow",
                                   related_user=request.user,
                                   message_body="")

            return JsonResponse(dict(success=True, followed=created))
    else:
        return JsonResponse(dict(success=False, code='2301', message='Invalid operation'))


@login_first
def profile_chat_settings(request, target_id):
    """
    Check or update the chat settings
    :param request:
    :param target_id:
    :return:
    """
    # TODO: implement this


@http_decorators.require_GET
@login_first
def profile_authed_cars(request, user_id):
    """ 获取制定用户所有已经认证的跑车的信息, 返回的数据格式如下:
     -- success
     -- cars: array
       |-- car_info
          | car_id
          | name
          | logo
          | image
       |-- identified_date: 认证的时间
       |-- signature: 跑车签名
    """
    carsOwnerShip = SportCarOwnership.objects.select_related("car") \
        .filter(user_id=user_id).order_by("-created_at")
    cars_dict_data = map(lambda x: x.dict_description(), carsOwnerShip)
    return JsonResponse(dict(success=True, cars=cars_dict_data))

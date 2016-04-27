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
from .models import User, AuthenticationCode
from .forms import RegistrationForm, PasswordResetForm
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
        return JsonResponse(response_dict)


@http_decorators.require_POST
@post_data_loader()
def account_send_code(request, data):
    """ Request for authentication code
     POST params:
        - phone_num: phone number
    """
    phone_num = data.get('phone_num', None)
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
    user.birth_date = data['birth_date']
    user.star_sign = star_sign_from_date(user.birth_date)
    user.avatar = request.FILES['avatar']
    user.save()
    return JsonResponse(dict(success=True))

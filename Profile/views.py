# coding=utf-8
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators import http as http_decorators
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from django.utils import timezone

from .utils import send_sms, create_random_code
from .forms import RegistrationForm, PasswordResetForm, ProfileCreationForm, CorporationUserApplicationCreateForm
from .models import AuthenticationCode, UserFollow, UserRelationSetting
from Club.models import Club, ClubJoining
from Sportscar.models import Sportscar, SportCarOwnership
from Status.models import Status, StatusLikeThrough
from custom.utils import login_first, post_data_loader, page_separator_loader
#######################################################################################################################
#
# 以下是登陆注册部分使用的API
#
#######################################################################################################################


@http_decorators.require_POST
@post_data_loader()
def account_login(request, data):
    """ Login through this method
     This method only accept post request

     POST params:
        - username: username
        - password: password
    """
    username = data.get('username', '')
    password = data.get('password', '')
    user = auth.authenticate(username=username,
                             password=password)
    if user is None:
        if not get_user_model().objects.filter(username=username).exists():
            error_reason = 'invalid username'
            error_code = '1000'
        else:
            error_reason = 'password incorrect'
            error_code = '1001'
        return JsonResponse(dict(success=False, message=error_reason, code=error_code))
    else:
        auth.login(request, user)
        return JsonResponse(dict(success=True, userID=user.id))


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
def account_register(request, data):
    """ Create New user through this interface
     This method only accept post request
     POST params:
        - username: username, only accept phoneNum
        - password1: password
        - password2: confirm
        - auth_code: authentication code
    """
    form = RegistrationForm(data)
    if form.is_valid():
        form.save()
        # form验证通过保证了下面这个查询一定是存在的
        AuthenticationCode.objects.deactivate(code=data['auth_code'], phone=data['username'])
        new_user = auth.authenticate(username=data["username"], password=data["password1"])
        auth.login(request, new_user)
        return JsonResponse(dict(success=True, userID=new_user.id))
    else:
        response_dict = dict(success=False, code='1002')
        response_dict.update(form.errors)
        return JsonResponse(response_dict)


@http_decorators.require_POST
@post_data_loader()
def account_reset_password(request, data):
    """ Reset password
     The view only accept post request

     POST params:
        - username: username, only accept phoneNum
        - password1: password
        - password2: confirm
        - auth_code: authentication code
    """
    form = PasswordResetForm(data)
    if form.is_valid():
        form.save()
        new_user = auth.authenticate(username=data["username"], password=data["password1"])
        auth.login(request, new_user)
        AuthenticationCode.objects.deactivate(code=data['auth_code'], phone=data['username'])
        return JsonResponse(dict(success=True, userID=new_user.id))
    else:
        response_dict = dict(success=False)
        response_dict.update(form.errors)
        return JsonResponse(response_dict)


@http_decorators.require_POST
@login_first
@post_data_loader()
def account_profile(request, data):
    """ Set profile
     This view only accept POST request

     POST params:
        - nick_name:
        - gender:m or f
        - birth_date: birth date
        - avatar:
    """
    print request.FILES
    form = ProfileCreationForm(profile=request.user.profile, data=data, files=request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse(dict(success=True))
    else:
        response_dict = dict(success=False)
        response_dict.update(form.errors)
        return JsonResponse(response_dict)


#######################################################################################################################
#
# 以下是个人中心部分使用的API
#
#######################################################################################################################


@http_decorators.require_GET
@login_first
def profile_info(request, user_id):
    """ 获取个人中心首页的信息
     :param user_id  需要索取的用户信息对应用户的id，当这个id是当前登陆用户的id时，返回“我的”界面
                     需要的数据，否则返回“他人”界面需要的数据
     :return 需要返回的数据较为复杂：如下列出：
         -- success
         -- user_profile
          | nick_name:
          | age:
          | avatar:
          | gender:
          | star_sign:
          | district:
          | job:
          | interest:
          | signature:
          | -- avatar_car
             | car_id:
             | name:
             | logo:
             | image:
          | -- avatar_club
             | ..
          | status_num:
          | fans_num:
          | follow_num:
          | -- avatar_club
             | id:
             | club_logo:
             | club_name:
          | followed: 是否被当前登陆的用户关注了
        如果是返回他人的数据，还会增加一个字段：followed来表明当前登陆用户是否已经关注的了指定用户

        注意：
            在个人界面中用户实时位置的更新一集下方的对于动态列表的，汽车介绍等需要从别的接口单独获取
    """
    try:
        user = get_user_model().objects.select_related('profile__avatar_club', 'profile__avatar_car')\
            .get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=True, code='2000', message='User not found.'))
    profile = user.profile
    user_info = dict(
        userID=user.id,
        nick_name=profile.nick_name,
        age=profile.age,
        avatar=profile.avatar.url,
        gender=profile.get_gender_display(),
        star_sign=profile.get_star_sign_display(),
        district=profile.district,
        job=profile.job,
        signature=profile.signature,
    )
    user_info['status_num'] = Status.objects.filter(user=user).count()
    user_info['fans_num'] = UserFollow.objects.filter(target_user=user).count()
    user_info['follow_num'] = UserFollow.objects.filter(source_user=user).count()
    car = profile.avatar_car
    if car is not None:
        user_info['avatar_car'] = car.dict_description()
    club = profile.avatar_club
    if club is not None:
        user_info['avatar_club'] = club.dict_description()
    if user.id != request.user.id:
        user_info['followed'] = UserFollow.objects.filter(source_user=request.user, target_user=user).exists()
    return JsonResponse(dict(success=True, user_profile=user_info))


@http_decorators.require_POST
@login_first
def profile_corporation_user_authenticate(request):
    """ 企业用户申请提交
    """

    form = CorporationUserApplicationCreateForm({"user": request.user.id}, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse(dict(success=True))
    else:
        print(form.errors)
        return JsonResponse(dict(success=False))

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
    carsOwnerShip = SportCarOwnership.objects.select_related("car")\
        .filter(user_id=user_id).order_by("-created_at")
    cars_dict_data = map(lambda x: x.dict_description(), carsOwnerShip)
    return JsonResponse(dict(success=True, cars=cars_dict_data))


@http_decorators.require_GET
@login_first
@page_separator_loader
def profile_status_list(request, date_threshold, op_type, limit, user_id):
    """ 这个函数和状态列表的首页十分类似
     :param user_id 目标用户的id
    """
    if op_type == 'latest':
        date_filter = Q(created_at__gt=date_threshold)
    else:
        date_filter = Q(created_at__lt=date_threshold)

    car_query_id = request.GET.get("filter_car", None)
    if car_query_id is not None:
        car_query = Q(car_id=car_query_id)
    else:
        car_query = Q()

    data = Status.objects.filter(date_filter & car_query, user__id=user_id, deleted=False).order_by("-created_at")[0:limit]

    def format_fix(status):
        return status.dict_description()

    data = map(format_fix, data)
    # TODO: 这里还要返回status创建的时间
    return JsonResponse(dict(success=True, data=data))


@http_decorators.require_POST
@post_data_loader()
def profile_modify(request, data):
    """ data为修改的属性字典
    """
    modifiable_properties = ['nick_name', 'avatar', 'avatar_club', 'avatar_car', 'signature',
                             'job', 'district']
    # First, check if the posted data are valid
    for key in data:
        if key not in modifiable_properties:
            return JsonResponse(dict(success=False, code='2001', message='Invalid property name.'))

    profile = request.user.profile

    if 'avatar' in request.FILES:
        profile.avatar = request.FILES.get('avatar')

    profile.nick_name = data.get('nick_name', profile.nick_name)
    profile.signature = data.get('signature', profile.signature)
    profile.job = data.get('job', profile.job)
    profile.district = data.get('district', profile.district)

    try:
        if 'avatar_club' in data:
            join = ClubJoining.objects.get(user=request.user, club__id=data['avatar_club'])
            profile.avatar_club_id = join.club_id
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='2002',
                                 message='Club not found or you have not joined the club yet.'))

    try:
        if 'avatar_car' in data:
            ownership = SportCarOwnership.objects.get(user=request.user, car__id=data['avatar_car'], identified=True)
            profile.avatar_car_id = ownership.car_id
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, code='2003', message='Car not found or you do not own this car'))

    profile.save()
    response_dict = dict(success=True)
    if 'avatar' in request.FILES:
        response_dict["avatar"] = profile.avatar.url
    return JsonResponse(response_dict)


@http_decorators.require_GET
@page_separator_loader
def profile_fans_list(request, date_threshold, op_type, limit, user_id):
    """ 这个接口返回粉丝列表,GET参数中的user_id指定了用户,如果没有发现这个参数,则认为是获取当前用户粉丝列表
     返回为一个列表,其中每个用户返回头像,昵称,关注该用户的时间,id
    """
    try:
        user = get_user_model().objects.get(id=user_id)
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
            filter_q = filter_q | Q(source_user__profile__nick_name__icontains=filter_element)
    else:
        filter_q = Q()

    fans = UserFollow.objects.select_related('source_user__profile')\
        .filter(date_filter & filter_q, target_user=user)[0:limit]

    def data_organize(x):
        source_user = x.source_user
        recent_status = Status.objects.filter(user=source_user).order_by("-created_at").first()
        recent_status_des = ""
        if recent_status is not None and recent_status.content is not None:
            recent_status_des = recent_status.content
        return dict(
            userID=source_user.id,
            avatar=source_user.profile.avatar.url,
            created_at=x.created_at.strftime('%Y-%m-%d %H:%M:%S %Z'),
            nick_name=source_user.profile.nick_name,
            recent_status_des=recent_status_des
        )

    return JsonResponse(dict(success=True, fans=map(data_organize, fans)))


@http_decorators.require_GET
@page_separator_loader
def profile_follow_list(request, date_threshold, op_type, limit, user_id):
    """ 这个接口返回关注列表,GET参数中的user_id指定了用户,如果没有发现这个参数,则认为是获取当前用户粉丝列表
     返回为一个列表,其中每个用户返回头像,昵称,关注该用户的时间,id
    """
    try:
        user = get_user_model().objects.get(id=user_id)
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

    follows = UserFollow.objects.select_related('source_user__profile').filter(date_filter & filter_q, source_user=user)[0:limit]

    def data_organize(x):
        target_user = x.target_user
        recent_status = Status.objects.filter(user=target_user).order_by("-created_at").first()
        recent_status_des = ""
        if recent_status is not None and recent_status.content is not None:
            recent_status_des = recent_status.content
        return dict(
            userID=target_user.id,
            avatar=target_user.profile.avatar.url,
            time=x.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            nick_name=target_user.profile.nick_name,
            recent_status_des=recent_status_des
        )

    return JsonResponse(dict(success=True, follow=map(data_organize, follows)))



@http_decorators.require_POST
@post_data_loader()
def profile_operation(request, data, user_id):
    """ 用户操作,目前只限于关注
    """
    # TODO: 还需要取消关注
    if 'op_type' not in data or data['op_type'] not in ['follow']:
        return JsonResponse(dict(success=False, code='2300', message='No valid operation type param found.'))
    if int(user_id) == request.user.id:
        return JsonResponse(dict(success=False, message='Invalid operation', code='2301'))
    try:
        target_user = get_user_model().objects.get(id=user_id)
    except ObjectDoesNotExist:
        return JsonResponse(dict(success=False, message='User not found', code='2000'))

    if data['op_type'] == 'follow':
        obj, created = UserFollow.objects.get_or_create(source_user=request.user, target_user=target_user)
        if not created:
            obj.delete()
        return JsonResponse(dict(success=True, follow=created))


@http_decorators.require_GET
@login_first
@page_separator_loader
def profile_black_list(request, date_threshold, op_type, limit):
    """ 获取当前登陆用户的黑名单,这个方法还没有进行测试
    """
    if op_type == 'latest':
        date_filter = Q(blacklist_at__gt=date_threshold)
    else:
        date_filter = Q(blacklist_at__lt=date_threshold)

    search_filter = Q()
    filter_str = request.GET.get("filter", None)
    if filter_str is not None:
        filter_elements = filter_str.split(" ")  # 搜索关键词以空格分割
        for filter_element in filter_elements:
            search_filter = search_filter | Q(target__profile__nick_name__icontains=filter_element)

    users = UserRelationSetting.objects.select_related("user__profile", "target__profile")\
        .order_by("-blacklist_at").filter(date_filter & search_filter, user=request.user)[0:limit]

    def data_organize(x):
        result = x.dict_description()
        recent_status = Status.objects.filter(user=x.target).order_by("-created_at").first()
        recent_status_des = ""
        if recent_status is not None and recent_status.content is not None:
            recent_status_des = recent_status.content
        result["recent_status_des"] = recent_status_des
        return result

    return JsonResponse(dict(
        success=True,
        users=map(data_organize, users)
    ))


@http_decorators.require_POST
@login_first
@post_data_loader()
def profile_black_list_update(request, data):
    """ 更新的黑名单,上传参数形式为:
     | op_type: add/remove
     |-- users:
        |-- id: 只需要id
     只需要返回是否是成功

    """
    op_type = data["op_type"]
    if op_type == "add":
        id_list = data["users"]
        for user_id in id_list:
            try:
                target = get_user_model().objects.get(id=user_id)
            except ObjectDoesNotExist:
                return JsonResponse(dict(success=False, message="user with id:%s no found" % user_id, code="4001"))
            relation_setting = UserRelationSetting.objects.get_or_create(
                    user=request.user, target=target)[0]
            relation_setting.allow_see_status = False
            relation_setting.blacklist_at = timezone.now()
            relation_setting.save()
        return JsonResponse(dict(success=True))
    else:
        id_list = data["users"]
        UserRelationSetting.objects.filter(user=request.user, target_id__in=id_list).update(allow_see_status=True)
        return JsonResponse(dict(success=True))


##
#  获取ChatSettings
##
@login_first
def profile_chat_settings(request, target_id):
    """ 查看聊天设置
    """
    if request.method == "POST":
        print request.POST
        relation, _ = UserRelationSetting.objects.get_or_create(user=request.user, target_id=target_id)
        if "remark_name" in request.POST:
            relation.remark_name = request.POST.get("remark_name")
        if "allow_see_status" in request.POST:
            relation.allow_see_status = request.POST.get("allow_see_status")
        if "see_his_status" in request.POST:
            relation.see_his_stats = request.POST.get("allow_see_status")
        relation.save()
        return JsonResponse(dict(success=True))
    else:
        try:
            result = UserRelationSetting.objects.select_related("target__profile", "user__profile").get(
                user=request.user, target__id=target_id
            )
        except ObjectDoesNotExist:
            # 没有查到记录的话就返回默认的设置值
            target_user = get_user_model().objects.select_related("profile").get(id=target_id)
            default_settings = dict(
                target=target_user.profile.simple_dict_description(),
                user=request.user.profile.simple_dict_description(),
                allow_see_status=True,
                see_his_status=True,
                remark_name=target_user.profile.nick_name
            )
            return JsonResponse(dict(success=True, settings=default_settings))
        return JsonResponse(dict(
            success=True, settings=result.dict_description()
        ))


# coding=utf-8
import json

from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from custom.utils import login_first, post_data_loader
from .models import SettingCenter, Suggestion
# Create your views here.


@require_http_methods(["GET", "POST"])
@login_first
@post_data_loader()
def settings(request, data):
    """这个接口用来将用户的本地设置存储到服务器端,使得用户在更换手机登录以后设置能够保持一致,
     设置相关的字段为:
     - notification_accept   是否接受新通知, YES or NO
     - notification_sound    声音
     - notification_shake    振动
     - location_visible_to
     - blacklist             黑名单,返回的时候这个直接代表黑名单内容, post时add字段代表需要添加的, remove字段代表需要删除的,
                             注意这个需要json解析,使用data的字段的json_data来提取
       |- add []
       |- remove []          注意,先处理添加,再处理删除.因此如果add和remove数组中有重复的id的话, 其作用将会抵消

     注意: 你需要一次提交所有的设置内容,因为这个接口的本质,是对本地设置的云端备份
    """
    user = request.user
    settings = user.setting_center
    print data
    if request.method == 'POST':

        settings.notification_accept = data['notification_accept'] in ['YES', 'yes', 'y', 'Y']
        settings.notification_sound = data['notification_sound'] in ['YES', 'yes', 'y', 'Y']
        settings.notification_shake = data['notification_shake'] in ['YES', 'yes', 'y', 'Y']
        if data['location_visible_to'] in ['all', 'female_only', 'male_only', 'none', 'only_idol', 'only_friend']:
            settings.location_visible_to = data['location_visible_to']
        if data['accept_invitation'] in ['all', 'friend', 'follow', 'fans', 'auth_first', 'never']:
            settings.accept_invitation = data['accept_invitation']
        settings.show_on_map = data["show_on_map"] in ['YES', 'yes', 'y', 'Y']
        # blacklist = json.loads(data['blacklist'])
        # if 'add' in blacklist:
        #     add = list(get_user_model().objects.filter(id__in=blacklist['add']))
        #     settings.blacklist.add(*add)
        # if 'remove' in blacklist:
        #     remove = list(get_user_model().objects.filter(id__in=blacklist['remove']))
        #     settings.blacklist.remove(*remove)
        settings.save()

        return JsonResponse(dict(success=True))

    # 返回当前的设置
    blacklist = settings.blacklist.all().values_list('id', flat=True)
    result = dict(
        notification_accept=settings.notification_accept,
        notification_shake=settings.notification_shake,
        notification_sound=settings.notification_sound,
        location_visible_to=settings.location_visible_to,
        accept_invitation=settings.accept_invitation,
        show_on_map=settings.show_on_map,
        blacklist=blacklist if len(blacklist) != 0 else None
    )
    return JsonResponse(dict(success=True, settings=result))


@require_POST
@login_first
@post_data_loader()
def give_suggestions(request, data):
    """ 这个接口用来提交用户的反馈
    """
    Suggestion.objects.create(content=data['content'], user=request.user)
    return JsonResponse(dict(success=True))

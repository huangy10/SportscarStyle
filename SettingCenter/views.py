# coding=utf-8
from django.views.decorators.http import require_http_methods

from custom.utils import login_first
# Create your views here.


@require_http_methods(["GET", "POST"])
@login_first
def settings(request, data):
    """这个接口用来将用户的本地设置存储到服务器端,使得用户在更换手机登录以后设置能够保持一致
    """
    pass

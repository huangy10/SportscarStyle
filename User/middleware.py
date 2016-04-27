from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from User.utils import JWTUtil
from .models import User
from Notification.models import RegisteredDevices

class MyJWTAuthorizationMiddleware(object):

    def process_request(self, request):
        if not hasattr(request, '_cached_user'):
            request._cached_user = self.get_user(request)
        request.user = request._cached_user

    def get_user(self, request):
        header = request.META.get("HTTP_AUTHORIZATION")
        print header
        if header is None:
            return None
        data = JWTUtil.jwt_decode(header)
        print data
        if data is None:
            return None
        user_id = data['user_id']
        device_id = data['device_id']
        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
        if RegisteredDevices.objects.filter(user=user, device_id=device_id, is_active=True).exists():
            return user
        else:
            return None

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from User.utils import JWTUtil
from .models import User
from Notification.models import RegisteredDevices

class MyJWTAuthorizationMiddleware(object):

    def process_request(self, request):
        if not hasattr(request, '_cached_user') or not hasattr(request, '_cached_device'):
            user, device = self.get_user(request)
            request._cached_user = user
            request._cached_device = device
        request.user = request._cached_user
        request.device = request._cached_device

    def get_user(self, request):
        header = request.META.get("HTTP_AUTHORIZATION")
        if header is None:
            return None, None
        data = JWTUtil.jwt_decode(header)
        if data is None:
            return None, None
        user_id = data['user_id']
        device_id = data['device_id']
        try:
            user = User.objects.get(pk=user_id)
            device = RegisteredDevices.objects.get(
                token=device_id, is_active=True, user=user
            )
        except ObjectDoesNotExist:
            return None, None

        return user, device


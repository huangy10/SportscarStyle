from django.core.exceptions import ObjectDoesNotExist

from .models import User


class SSAutehenticationBackend(object):
    """
     Authentication Backend of my own User model
    """

    def authenticate(self, username=None, password=None):
        if username is None or password is None:
            return None
        try:
            user = User.objects.filter(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

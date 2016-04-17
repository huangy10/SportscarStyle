import sys
import os

from tornado.concurrent import Future
from django.core.wsgi import get_wsgi_application
sys.path.extend([os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SportscarStyle.settings')
application = get_wsgi_application()

from django.utils import timezone
from Chat.models import ChatRecordBasic
from Chat.ChatServer.redis_access import *

class MessageFuture(Future):
    """
    Future object with two more attributes added
    """

    def __init__(self, user_id):
        self.user_id = user_id
        super(MessageFuture, self).__init__()


class MessageDispatch(object):

    def wait_for_message(self, user_id):
        user = UserRedisAccess(user_id)
        result_future = MessageFuture(user_id=user_id)
        last_access = user.last_access
        if last_access is not None:
            new_messages = ChatRecordBasic.objects.filter(
                created_at__gt=last_access
            )
            if new_messages.exists():
                result_future.set_result(list(new_messages))
        user.wait(timezone.now())

    def cancel_wait(self, future):
        user = UserRedisAccess(future.user_id)
        user.cancel_wait()
        future.set_result([])

    def new_message(self, message):
        pass

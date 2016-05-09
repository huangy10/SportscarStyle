# coding=utf-8
import sys
import os
import json
import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from tornado.web import RequestHandler, Application
from tornado import ioloop, gen

from django.core.wsgi import get_wsgi_application

sys.path.extend([os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir))])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SportscarStyle.settings')
application = get_wsgi_application()

from Notification.redis_operation import UnreadUtil
from Chat.ChatServer.dispatch import MessageDispatch
from Chat.models import Chat, ChatEntity
from Club.models import Club
from Notification.models import RegisteredDevices, Notification
from User.models import User
from User.utils import JWTUtil

_dispatcher = MessageDispatch()


def get_global_dispatcher():
    return _dispatcher


class JsonResponseHandler(RequestHandler):

    @property
    def dispatcher(self):
        global _dispatcher
        return _dispatcher

    def __init__(self, application, request, **kwargs):
        self.device = None
        super(JsonResponseHandler, self).__init__(application, request, **kwargs)

    def get_current_user(self):
        header = self.request.headers.get('AUTHORIZATION')
        if header is None:
            return None
        data = JWTUtil.jwt_decode(header)
        if data is None:
            return None
        user_id = data['user_id']
        device_id = data['device_id']
        try:
            user = User.objects.get(pk=user_id)
            device = RegisteredDevices.objects.get(
                token=device_id,
                is_active=True,
                user=user
            )
        except ObjectDoesNotExist:
            return None
        self.device = device
        return user

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def JSONResponse(self, data):
        self.write(json.dumps(data))


class ChatUpdateHandler(JsonResponseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        user = self.current_user
        device = self.device
        print "User {0} start waiting for message on device: {1}".format(
            user.username, device.token
        )
        if user is None or device is None:
            self.JSONResponse(dict(success=False, message='You need to login first', code='1402'))
            return
        # Synchronous the unread numbers here
        client_unread_num = self.get_argument("unread", default=0)
        # Notice that if the client_unread_num is bigger than or equal to the unread data saved in redis server,
        # the following command takes no effect.
        UnreadUtil.set(user.id, client_unread_num)
        cur_focus_chat = self.get_argument("focused", default=None)

        if user is None or device is None:
            self.JSONResponse(dict(success=False, message='You need to login first', code='1402'))
            return
        messages = yield self.dispatcher.wait_for_message(device, cur_focused_entity=cur_focus_chat)
        print "user: {0} receive message: {1}".format(user.username, messages)
        if self.request.connection.stream.closed():
            self.JSONResponse(dict(success=False))
            return
        self.JSONResponse(dict(success=True, data=messages))

    def on_connection_close(self):
        print "disconnect: {}".format(self.current_user.username)
        if self.device is None:
            return
        self.dispatcher.cancel_wait(self.device)


class ChatNewHandler(JsonResponseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        发布一条新的聊天信息,需要上传的参数为
          | chat_type: private or group
          | target_id: when the chat_type is "private", this id refers to a target user, or a club when club when "group"
          | message_type: text, image, voice, activity, share or contact
               | image: for image
               | text_content: for text
               | audio: for voice
               | text_content: for share
               | related_id: for activity and contact

        返回时告知是否发布成功以及这条消息的id
          ---
           |- success
           |- chat_record_id
        """
        user = self.current_user
        device = self.device
        if user is None or device is None:
            return self.JSONResponse(dict(success=False, message='You need to login first', code='1402'))
        chat_type = self.get_argument("chat_type")
        target_id = int(self.get_argument("target_id"))
        message_type = self.get_argument("message_type")
        creation_param = {
            "sender": user,
            "chat_type": chat_type,
            "message_type": message_type
        }

        if chat_type == "user":
            target_user = User.objects.get(id=target_id)
            creation_param["target_user"] = target_user
        elif chat_type == 'club':
            target_club = Club.objects.get(id=target_id)
            creation_param["target_club"] = target_club
        else:
            self.JSONResponse(dict(success=False, message="Undefined chat type"))
            return

        if message_type == "text":
            creation_param["text"] = self.get_argument('text_content')
        elif message_type == "image":
            file_info = self.request.files['image'][0]
            file_io = StringIO.StringIO(file_info["body"])
            image = InMemoryUploadedFile(
                file=file_io, field_name=None, name=file_info["filename"], content_type=file_info["content_type"],
                size=file_io.len, charset=None
            )
            creation_param["image"] = image

        elif message_type == "audio":
            file_info = self.request.files['audio'][0]
            file_io = StringIO.StringIO(file_info["body"])
            audio = InMemoryUploadedFile(
                file=file_io, field_name=None, name=file_info["filename"], content_type=file_info["content_type"],
                size=file_io.len, charset=None
            )
            creation_param['audio'] = audio
        elif message_type == "activity":
            related_id = self.get_argument("related_id")
            creation_param['related_id'] = related_id
        message = Chat.objects.create(**creation_param)
        message.save()
        self.dispatcher.new_message(message)
        self.JSONResponse(dict(success=True, chat_record_id=message.id))


class NewNotificationHanlder(JsonResponseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        notif_id = self.get_argument("id")
        try:
            notif = Notification.objects.get(pk=notif_id)
        except ObjectDoesNotExist:
            self.JSONResponse(dict(success=False))
            return
        self.dispatcher.new_message(notif)
        self.JSONResponse(dict(success=True))


def start_tornado_service():

    app = Application(
        [
            (r"/chat/update", ChatUpdateHandler),
            (r"/chat/speak", ChatNewHandler)
        ],
        cookie_secret="463a2380-39c9-450a-a884-3f7b8857d720",
        xsrf_cookies=False,
        debug=True
    )
    app.listen(port=8888)

    app2 = Application(
        [
            (r"/notification/internal", NewNotificationHanlder),
        ],
        cookie_secret="463a2380-39c9-450a-a884-3f7b8857d720",
        xsrf_cookies=False,
        debug=True)
    app2.listen(address="localhost", port=8887)

    ioloop.IOLoop.current().start()

if __name__ == "__main__":
    start_tornado_service()

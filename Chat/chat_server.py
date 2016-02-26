#!coding=utf-8
# 这个文件利用tornado引擎来驱动支持聊天部分的功能

import sys
import os
import json
import StringIO

from tornado.web import RequestHandler, Application
from tornado import ioloop, gen
from tornado.concurrent import Future

from django.core.wsgi import get_wsgi_application
sys.path.extend([os.path.abspath(os.path.join(os.getcwd(), os.pardir))])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SportscarStyle.settings')
application = get_wsgi_application()

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from SportscarStyle.celery import app
from celery.contrib.methods import task_method
from Chat.models import ChatRecordBasic
from Club.models import Club
from tasks import inform_of_related_waiters


class MessageFuture(Future):
    """ 派生了Future类型, 增加了两个属性,
    """

    def __init__(self, user_id, waiting_date):
        super(MessageFuture, self).__init__()
        self.user_id = user_id
        self.waiting_date = waiting_date


class MessageDispatch(object):
    """ 消息调度器
    """

    def __init__(self):
        # 正在等待新消息的用户, 以user_id为键值
        self.waiters = dict()

    def wait_for_message(self, user_id, waiting_date=None):
        """ 将一个用户注册为新消息的监听者
         我们创建了一个Future对象来实现
        """
        result_future = MessageFuture(user_id=user_id, waiting_date=waiting_date)
        if waiting_date is not None:
            new_messages = ChatRecordBasic.objects.filter(created_at__gt=waiting_date)
            if new_messages.count() > 0:
                # 如果已经发现了现有的消息,则直接返回这个结果即可
                result_future.set_result(new_messages)
                return result_future
            # 否则加入等待队列
        self.waiters[user_id] = result_future
        return result_future

    def cancel_wait(self, future):
        del self.waiters[future.user_id]
        future.set_result([])

    # @app.task(filter=task_method, name="message_dispatch.new_mewssage")
    def new_message(self, message):
        """
         :param message 新的消息
        """
        # 用celery来异步完成这一操作
        global global_message_dispatch
        inform_of_related_waiters(message, global_message_dispatch)


# 全局唯一的调度器
global_message_dispatch = MessageDispatch()


class JSONResponseHandler(RequestHandler):

    def get_current_user(self):
        session_key = self.get_cookie("sessionid", None)
        if session_key is None:
            return None
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get("_auth_user_id")
        user = get_user_model().objects.get(id=uid)
        return user

    def set_default_headers(self):
        # 总是返回json响应
        self.set_header("Content-Type", 'application/json')

    def JSONResponse(self, dict):
        self.write(json.dumps(dict))


class ChatUpdateHandler(JSONResponseHandler):

    def __init__(self, application, request, **kwargs):
        super(ChatUpdateHandler, self).__init__(application, request, **kwargs)
        self.future = None

    @gen.coroutine
    def post(self, *args, **kwargs):
        """ 更新聊天信息
        """
        waiting_date = timezone.now()
        if self.current_user is None:
            self.JSONResponse(dict(success=False, message='You need to login first', code='1402'))
            return
        self.future = global_message_dispatch.wait_for_message(self.current_user.id, waiting_date=waiting_date)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.JSONResponse(dict(success=True, messages=map(lambda x: x.dict_description(), messages)))

    def on_connection_close(self):
        if self.future is None:
            return
        print(self.future)
        global_message_dispatch.cancel_wait(self.future)


class ChatNewHandler(JSONResponseHandler):
    """ 发送新的消息
    """

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
        if self.current_user is None:
            return self.JSONResponse(dict(success=False, message='You need to login first', code='1402'))
        chat_type = self.get_argument("chat_type")
        target_id = int(self.get_argument("target_id"))
        message_type = self.get_argument("message_type")
        creation_param = {
            "sender": self.current_user,
            "chat_type": chat_type,
            "message_type": message_type
        }
        if chat_type == "private":
            creation_param["target_user"] = get_user_model().objects.get(id=target_id)
        else:
            creation_param["target_club"] = Club.objects.get(id=target_id)
        message = ChatRecordBasic.objects.create(**creation_param)

        if message_type == "text":
            message.text_content = self.get_argument("text_content")
        elif message_type == "image":
            file_info = self.request.files['image'][0]
            file_io = StringIO.StringIO(file_info["body"])
            message.image = InMemoryUploadedFile(
                file=file_io, field_name=None, name=file_info["filename"], content_type=file_info["content_type"],
                size=file_io.len, charset=None
            )
        elif message_type == "audio":
            file_info = self.request.files['audio'][0]
            file_io = StringIO.StringIO(file_info["body"])
            message.audio = InMemoryUploadedFile(
                file=file_io, field_name=None, name=file_info["filename"], content_type=file_info["content_type"],
                size=file_io.len, charset=None
            )
        elif message_type == "activity":
            message.related_id = self.get_argument("related_id")

        message.save()
        global_message_dispatch.new_message(message)
        return self.JSONResponse(dict(success=True, message=message.dict_description()))


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
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_tornado_service()
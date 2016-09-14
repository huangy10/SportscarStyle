# coding=utf-8
import json
import os
import sys
import redis
from django.core.exceptions import ObjectDoesNotExist
from django.core.wsgi import get_wsgi_application
from tornado import gen
from tornado.concurrent import Future

from User.models import User

sys.path.extend([os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir))])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SportscarStyle.settings')
application = get_wsgi_application()

from Chat.models import Chat, ChatEntity
from Club.models import Club, ClubJoining
from Notification.models import Notification, RegisteredDevices
from Notification.tasks import push_notification
from .utils import MessageList as List


r = redis.Redis(db=11, host='localhost', port=6379)


class Waiter(object):

    CACHE_SIZE = 128

    def __init__(self, device, future):
        self.device = device
        self.future = future
        self.cur_focused_entity = None
        self._cached_messages = None

    @property
    def cache(self):
        if self._cached_messages is not None:
            return self._cached_messages
        self._cached_messages = List(key="{0}".format(self.device.user.id), db=r)
        return self._cached_messages

    @property
    def has_cache(self):
        return len(self.cache) > 0

    @classmethod
    def cache_chat(cls, message, user):
        """
         util method to cache messages
        :param message:
        :param user:
        :return:
        """
        if isinstance(message, dict):
            message = json.dumps(message)
        if not isinstance(message, basestring):
            raise ValueError
        cache = List(key="{0}".format(user.id), db=r)
        cache.append(message)

    def take_response(self, message):
        if isinstance(message, list):
            self.future.set_result(message)
        else:
            self.future.set_result([message])


class MessageFuture(Future):
    def __init__(self, user_id):
        self.user_id = user_id
        super(MessageFuture, self).__init__()


class Singleton(type):

    _instance = {}

    def __call__(cls, *more):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*more)
        return cls._instance[cls]

    # def __call__(cls, *args, **kwargs):
    #     if cls not in cls._instance:
    #         cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    #     return cls._instance[cls]


class MessageDispatch(object):

    __metaclass__ = Singleton

    def __init__(self):
        # use the id of the device as the key
        self.waiters = dict()

    def wait_for_message(self, device, cur_focused_entity=None):
        # create a future
        future = MessageFuture(user_id=device.user.id)
        waiter = self.waiters.get(device.id)
        if cur_focused_entity is not None:
            cur_focused_entity = int(cur_focused_entity)

        if waiter is not None:
            # if the waiter is already in the waiting list, release the old future object and set the new
            if waiter.future is not None and not waiter.future.done():
                waiter.future.set_result([])
            waiter.future = future
            if waiter.cur_focused_entity != cur_focused_entity:
                # if a the current focused entity changed, clear the unread number of the new one
                if cur_focused_entity is not None:
                    try:
                        entity = ChatEntity.objects.get(pk=cur_focused_entity)
                        if entity.unread_num > 0:
                            entity.unread_num = 0
                            entity.save()
                        waiter.cur_focused_entity = cur_focused_entity
                    except ObjectDoesNotExist:
                        waiter.cur_focused_entity = None
                else:
                    waiter.cur_focused_entity = None
        else:
            # if the waiter is not in the waiting list, create one
            waiter = Waiter(device=device, future=future)
            waiter.cur_focused_entity = cur_focused_entity
            if cur_focused_entity is not None:
                try:
                    entity = ChatEntity.objects.get(pk=cur_focused_entity)
                    if entity.unread_num > 0:
                        entity.unread_num = 0
                        entity.save()
                    waiter.cur_focused_entity = cur_focused_entity
                except ObjectDoesNotExist:
                    waiter.cur_focused_entity = None
            self.waiters[device.id] = waiter

        # Check if there is messages caching in the redis server. If so, send it to the waiter immediately
        if waiter.has_cache:
            future.set_result(waiter.cache.pack_to_json())

        return future

    def cancel_wait(self, device):
        waiter = self.waiters[device.id]
        if waiter is None:
            return
        else:
            waiter.cur_focused_entity = None
        if waiter.future is not None and not waiter.future.done():
            waiter.future.set_result([])
        waiter.future = None

    def logout(self, device):
        self.cancel_wait(device)
        self.waiters[device.id] = None

    def new_message(self, message):
        if message is None:
            return
        if isinstance(message, Chat):
            # asynchronous
            gen.Task(self.handle_new_chat, chat=message)
            # synchronous
            # self.handle_new_chat(chat=message, callback=None)
        elif isinstance(message, Notification):
            # self.handle_new_notification(message, callback=None)
            gen.Task(self.handle_new_notification, notification=message)
        elif isinstance(message, basestring):
            pass

    def general_json_message_handler(self, message):
        """
         You can use this method to "push" any kind of data to the user, the message is a json-serialized
         string. The json-data should be
          - target_user: id of the target user
          - payload: actual data you want to send

         :param message:
        :return:
        """
        try:
            data = json.loads(message)
            user_id = data["target_user"]
            payload = data["payload"]
        except ValueError:
            # log here
            return
        try:
            target_user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            # log here
            return
        # find all active devices belong to this user
        activate_devices = RegisteredDevices.objects.filter(user=target_user, is_active=True)
        for device in activate_devices:
            waiter = self.waiters.get(device.id)
            if waiter is not None and waiter.future is not None and not waiter.future.done():
                waiter.take_response(payload)

    def handle_new_chat(self, chat, callback):

        if chat is None:
            return
        if chat.chat_type == 'user':

            target_user = chat.target_user
            activate_devices = RegisteredDevices.objects.filter(user=target_user, is_active=True)
            entity, created = ChatEntity.objects.get_or_create(host=target_user, user=chat.sender)
            # make sure the reversed entity exists, too
            ChatEntity.objects.get_or_create(host=chat.sender, user=target_user)

            tokens = []
            badge = 1
            for device in activate_devices:
                waiter = self.waiters.get(device.id)
                if waiter is not None and waiter.future is not None and not waiter.future.done():
                    # if waiter is online
                    entity_response = entity.dict_description()
                    if waiter.cur_focused_entity == entity.id:
                        # if the message belongs to the currently focused chat, then drop the unread increase
                        badge = 0
                        entity_response["unread_num"] = 0
                    else:
                        entity_response["unread_num"] += badge

                    response = chat.dict_description(host=target_user)
                    response.update(roster=entity_response)
                    waiter.take_response(response)

                elif waiter is not None:
                    response = chat.dict_description(host=target_user)
                    response.update(roster=entity.dict_description())
                    Waiter.cache_chat(response, target_user)
                tokens.append(device.token)
            if badge > 0:
                entity.unread_num += 1
                entity.save()
            elif entity.unread_num > 0:
                entity.unread_num = 0
                entity.save()
            if not entity.no_disturbing:
                push_notification.delay(
                    target_user, tokens, badge, message_body=chat.message_body_des, type='chat'
                )
        else:
            target_club = chat.target_club
            target_joins = ClubJoining.objects.filter(club=target_club)
            for join in target_joins:
                user = join.user
                if user.id == chat.sender_id:
                    continue
                # collect devices
                activate_devices = RegisteredDevices.objects.filter(user=user, is_active=True)
                entity, created = ChatEntity.objects.get_or_create(host=user, club=target_club)
                tokens = []
                badge = 1
                for device in activate_devices:
                    waiter = self.waiters.get(device.id)
                    if waiter is not None and waiter.future is not None and not waiter.future.done():
                        entity_response = entity.dict_description()
                        if waiter.cur_focused_entity == entity.id:
                            badge = 0
                            entity_response["unread_num"] = 0
                        else:
                            entity_response["unread_num"] += badge
                        response = chat.dict_description(host=user)
                        response.update(roster=entity.dict_description())
                        waiter.take_response(response)
                    elif waiter is not None:
                        response = chat.dict_description(host=user)
                        response.update(roster=entity.dict_description())
                        Waiter.cache_chat(response, user)
                    tokens.append(device.token)

                if badge > 0:
                    entity.unread_num += 1
                    entity.save()
                elif entity.unread_num > 0:
                    entity.unread_num = 0
                    entity.save()
                if not entity.no_disturbing:
                    push_notification.delay(
                        user, tokens, badge, message_body=chat.message_body_des, type='chat'
                    )
        if callback is not None:
            callback()

    def handle_new_notification(self, notification, callback):
        user = notification.target
        devices = RegisteredDevices.objects.filter(user=user, is_active=True)
        tokens = []
        badge = 1
        for device in devices:
            print device.id, self.waiters
            waiter = self.waiters.get(device.id)
            print waiter
            if waiter is not None and waiter.future is not None and not waiter.future.done():
                waiter.take_response(notification.dict_description())
                # badge = 0
            elif waiter is not None:
                Waiter.cache_chat(notification.dict_description(), user)
            tokens.append(device.token)
        if user.setting_center.notification_accept:
            push_notification.delay(
                user, tokens, badge, notification.apns_des(), 'notif'
            )
        if callback is not None:
            callback()




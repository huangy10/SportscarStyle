# coding=utf8

from SportscarStyle.celery import app

from Club.models import Club, ClubJoining
from Notification.tasks import push_notification
from Notification.models import RegisteredDevices

def inform_of_related_waiters(message, global_message_dispatch):
    """ 根据给定的message内容,通知所有的相关的用户通知相
     :param message
    """
    # 复制一份当前的等待列表以免冲突
    if message is None:
        return
    waiters = global_message_dispatch.waiters.copy()
    if message.chat_type == "private":
        # private: 私信,目标是单一用户
        target_waiter = waiters.get(message.target_id, None)
        if target_waiter is not None:
            target_waiter.set_result([message])
        else:
            tokens = RegisteredDevices.objects.filter(user=message.target_user, is_active=True)\
                .values_list("token", flat=True)
            push_notification.delay(message.target_user, tokens, 1, message_body=message.message_body_des())
    else:
        # group,群聊
        target_club = Club.objects.get(id=message.target_id)
        target_joins = ClubJoining.objects.filter(club=target_club)
        print "waiters", waiters
        print target_joins.values("user_id")
        for join in target_joins:
            user = join.user
            waiter = waiters.get(user.id, None)
            if message.sender == user:
                # 不需要讲消息发送给消息的发送者
                continue
            if waiter is not None:
                print message.target_id, "receive"
                waiter.set_result([message])
            else:
                print user.id, "unread"
                join.unread_chats += 1
                join.save()
                # TODO: 当目标用户不是waiter时,需要发送notification

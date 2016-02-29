# coding=utf8

from SportscarStyle.celery import app

from Club.models import Club

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
            # TODO: 当目标用户不是waiter时,需要发送notification
            pass
    else:
        # group,群聊
        target_club = Club.objects.get(id=message.target_id)
        target_users = target_club.members.all()
        for user in target_users:
            waiter = waiters.get(user.id, None)
            if waiter is not None:
                print message
                waiter.set_result([message])
            else:
                # TODO: 当目标用户不是waiter时,需要发送notification
                pass